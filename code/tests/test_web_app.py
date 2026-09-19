import json
import shutil
from pathlib import Path
from threading import Thread
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import pytest

from rwa_web.catalog import CatalogError, DataCatalog
from rwa_web.server import RwaWebServer
from rwa_engine.config_io import PROJECT_ROOT


DATASET_ID = "2026-08-31/v1.0.0"
DATA_ROOT = PROJECT_ROOT / "daten" / "rechenlaeufe"


def test_catalog_lists_inputs_runs_and_metrics():
    catalog = DataCatalog(DATA_ROOT)
    ids = {item["id"] for item in catalog.datasets()}
    assert DATASET_ID in ids
    detail = catalog.detail(DATASET_ID)
    assert len(detail["inputs"]) == 16
    assert detail["manifest"]["missing_inputs"] == []
    assert detail["manifest"]["changed_inputs"] == []
    assert detail["manifest"]["row_count"] > 0
    assert detail["runs"][0]["metrics"]["TREA"] > 0


@pytest.mark.parametrize("identifier", ["../secret", "2026-08-31/../../secret", "/etc/passwd", "x/y/z"])
def test_catalog_rejects_path_traversal(identifier):
    with pytest.raises(CatalogError):
        DataCatalog(DATA_ROOT).dataset_path(identifier)


@pytest.fixture
def web_server(tmp_path):
    # HTTP run tests must never create extra runs in published reference datasets.
    data_root = tmp_path / "datasets"
    shutil.copytree(DATA_ROOT, data_root)
    server = RwaWebServer(("127.0.0.1", 0), data_root)
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_port}"
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)


def test_http_health_dataset_and_static(web_server):
    with urlopen(f"{web_server}/api/health", timeout=5) as response:
        assert json.load(response) == {"status": "ok"}
    query = urlencode({"dataset": DATASET_ID})
    with urlopen(f"{web_server}/api/dataset?{query}", timeout=5) as response:
        assert json.load(response)["id"] == DATASET_ID
    with urlopen(f"{web_server}/", timeout=5) as response:
        assert b"RWA Control Center" in response.read()


def test_http_rejects_invalid_run_request(web_server):
    request = Request(f"{web_server}/api/run", data=json.dumps({"dataset": "../bad"}).encode(),
                      headers={"Content-Type": "application/json"}, method="POST")
    with pytest.raises(HTTPError) as error:
        urlopen(request, timeout=5)
    assert error.value.code == 400


def test_http_executes_existing_dataset_and_downloads_output(web_server):
    request = Request(f"{web_server}/api/run", data=json.dumps({"dataset": DATASET_ID}).encode(),
                      headers={"Content-Type": "application/json"}, method="POST")
    with urlopen(request, timeout=120) as response:
        body = json.load(response)
    assert body["status"] == "CALCULATED"
    run_id = body["run_id"]
    run = next(item for item in body["dataset"]["runs"] if item["run_id"] == run_id)
    assert run["controls_passed"] == run["control_count"] == 12
    query = urlencode({"dataset": DATASET_ID, "area": "output", "run": run_id,
                       "file": run["files"][0]["name"]})
    with urlopen(f"{web_server}/files?{query}", timeout=120) as response:
        assert response.headers.get_content_type() == \
               "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        assert response.read(2) == b"PK"
