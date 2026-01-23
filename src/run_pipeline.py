# src/run_pipeline.py

from pathlib import Path
import pandas as pd

from src.extract_tables import extract_transactions_from_pdf
from src.clean_rules import (
    drop_non_transaction_rows,
    parse_amount,
    to_numeric,
    finalize_schema,
)

RAW_DIR = Path("data/raw")
CLEAN_DIR = Path("data/clean")


def run_pipeline():
    CLEAN_DIR.mkdir(parents=True, exist_ok=True)

    pdf_files = sorted(RAW_DIR.glob("bank_statement_demo*.pdf"))

    for pdf_file in pdf_files:
        print(f"Processing: {pdf_file.name}")

        # 1. Extract
        df = extract_transactions_from_pdf(pdf_file)

        if df.empty:
            print(f"⚠️ No transactions found in {pdf_file.name}")
            continue

        # 2. Clean
        df = drop_non_transaction_rows(df)
        df = to_numeric(df)
        df = parse_amount(df)
        df = finalize_schema(df)

        # 3. Save
        out_path = CLEAN_DIR / f"{pdf_file.stem}_clean.csv"
        df.to_csv(out_path, index=False)

        print(f"Saved: {out_path.name} ({len(df)} rows)")


if __name__ == "__main__":
    run_pipeline()
