# src/extract_tables.py

from pathlib import Path
import pdfplumber
import pandas as pd


RAW_DIR = Path("data/raw")
INTERIM_DIR = Path("data/interim")


def extract_transactions_from_pdf(pdf_path: Path) -> pd.DataFrame:
    """
    Extract raw transaction rows from a single bank statement PDF.
    This function does NOT clean data. It only extracts rows.
    """
    rows = []

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()

            for table in tables:
                if not table or len(table) < 2:
                    continue

                header = [cell.lower() if cell else "" for cell in table[0]]

                # Heuristic: detect transaction table
                if "date" in header and "description" in header:
                    for raw_row in table[1:]:
                        if not raw_row or all(cell is None or cell == "" for cell in raw_row):
                            continue

                        rows.append({
                            "date": raw_row[0],
                            "description": raw_row[1],
                            "debit": raw_row[2],
                            "credit": raw_row[3],
                            "balance": raw_row[4],
                            "source_file": pdf_path.name,
                        })

    return pd.DataFrame(rows)


def batch_extract():
    INTERIM_DIR.mkdir(parents=True, exist_ok=True)

    pdf_files = sorted(RAW_DIR.glob("bank_statement_demo*.pdf"))

    for pdf_file in pdf_files:
        print(f"Extracting: {pdf_file.name}")
        df = extract_transactions_from_pdf(pdf_file)

        out_path = INTERIM_DIR / f"{pdf_file.stem}_extracted.csv"
        df.to_csv(out_path, index=False)

        print(f"Saved: {out_path.name} ({len(df)} rows)")


if __name__ == "__main__":
    batch_extract()
