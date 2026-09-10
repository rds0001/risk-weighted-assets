"""Kommandozeilenschnittstelle."""

from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path
import sys

from .contracts import TABLE_SPECS
from .config_io import PROJECT_ROOT
from .excel_io import write_input_workbooks
from .pipeline import RunRejected, run_dataset
from .synthetic import generate_synthetic_dataset


def _date(value: str) -> date:
    return date.fromisoformat(value)


def parser() -> argparse.ArgumentParser:
    p=argparse.ArgumentParser(prog="rwa",description="CRR-III/ICAAP Gesamt-Rechenlösung")
    sub=p.add_subparsers(dest="command",required=True)
    template=sub.add_parser("templates",help="Leere kanonische Excel-Templates erzeugen")
    template.add_argument("--output",type=Path,default=Path("templates/v1.0.0"))
    gen=sub.add_parser("generate",help="Synthetischen Bankdatensatz erzeugen")
    gen.add_argument("--data-root",type=Path,default=PROJECT_ROOT/"daten"/"rechenlaeufe");gen.add_argument("--as-of-date",type=_date)
    gen.add_argument("--version");gen.add_argument("--seed",type=int)
    gen.add_argument("--bank-profile",default="MID_SIZE_UNIVERSAL")
    run=sub.add_parser("run",help="Vorhandenen Datensatz vollständig rechnen")
    run.add_argument("--dataset",type=Path,required=True)
    allp=sub.add_parser("all",help="Synthetische Daten erzeugen und alle Rechnungen in einem Zug ausführen")
    allp.add_argument("--data-root",type=Path,default=PROJECT_ROOT/"daten"/"rechenlaeufe");allp.add_argument("--as-of-date",type=_date)
    allp.add_argument("--version");allp.add_argument("--seed",type=int)
    allp.add_argument("--bank-profile",default="MID_SIZE_UNIVERSAL")
    return p


def main(argv: list[str] | None=None) -> None:
    args=parser().parse_args(argv)
    try:
        if args.command=="templates":
            import pandas as pd
            tables={name:pd.DataFrame(columns=spec.all_columns) for name,spec in TABLE_SPECS.items()}
            files=write_input_workbooks(args.output,tables);print(f"{len(files)} Templates: {args.output}")
        elif args.command=="generate":
            dataset=generate_synthetic_dataset(args.data_root,as_of=args.as_of_date,version=args.version,seed=args.seed,
                                               bank_profile=args.bank_profile);print(dataset)
        elif args.command=="run":
            print(run_dataset(args.dataset))
        else:
            dataset=generate_synthetic_dataset(args.data_root,as_of=args.as_of_date,version=args.version,seed=args.seed,
                                               bank_profile=args.bank_profile)
            print(run_dataset(dataset))
    except RunRejected as exc:
        print(f"REJECTED: {exc}",file=sys.stderr);raise SystemExit(2)
