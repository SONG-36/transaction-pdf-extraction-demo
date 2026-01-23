# Bank Statement PDF Cleanup Demo (Transaction Ledger Extraction)

This project demonstrates a **reusable data-cleaning pipeline** that converts **messy bank statement PDFs** into **analysis-ready transaction ledgers**.

It reflects a **real-world client scenario** where financial statements are delivered as formatted PDFs that are readable by humans, but **not usable for data analysis, accounting systems, or automation**.

---

## Problem

Bank statement PDFs typically contain:

* Visual layouts instead of structured data
* Separate Debit / Credit columns
* Balance rows mixed with transactions
* Opening balance and summary rows
* Currency symbols, commas, and formatting noise

Such files **cannot be directly imported** into accounting tools, spreadsheets, or analytics pipelines.

---

## Input

* PDF bank statements (single-page or multi-page)
* Each PDF contains a transaction table with:

  * Date
  * Description
  * Debit
  * Credit
  * Running balance

Example input:

```
data/raw/
├── bank_statement_demo01.pdf
├── bank_statement_demo02.pdf
├── bank_statement_demo03.pdf
└── bank_statement_demo04.pdf
```

---

## Output

Each PDF is converted into a **clean transaction ledger** with:

* One row per transaction
* Numeric amounts with correct sign
* Consistent column schema
* Source file traceability

Final output schema:

| Column        | Description                                                 |
| ------------- | ----------------------------------------------------------- |
| `date`        | Transaction date                                            |
| `description` | Transaction description                                     |
| `amount`      | Signed numeric amount (credit = positive, debit = negative) |
| `balance`     | Account balance after transaction                           |
| `source_file` | Original PDF file name                                      |

Example output:

```
data/clean/
├── bank_statement_demo01_clean.csv
├── bank_statement_demo02_clean.csv
├── bank_statement_demo03_clean.csv
└── bank_statement_demo04_clean.csv
```

---

## Cleaning Rules (Key Decisions)

### 1. Opening Balance Handling

Rows such as **“Opening Balance”** are intentionally excluded.

These rows represent **account state**, not transactional activity, and are therefore **not suitable for ledger-based analysis or aggregation**.

---

### 2. Debit / Credit Normalization

* Credit amounts → positive values
* Debit amounts → negative values
* Currency symbols and commas are removed

This ensures the `amount` column can be directly used for:

* Summation
* Cash flow analysis
* Expense categorization

---

### 3. Balance Preservation

The `balance` column is retained **for verification and reconciliation**, but is **not used to infer transaction amounts**.

---

## Pipeline Overview

1. Extract tables from PDF using layout-aware parsing
2. Normalize column names
3. Remove non-transaction rows
4. Convert debit / credit into signed numeric amounts
5. Enforce final schema and add source metadata
6. Export clean CSV files

---

## How to Run

```bash
python -m src.run_pipeline
```

All PDFs in `data/raw/` are processed automatically.

---

## Why This Demo Matters

This project mirrors **real client requests** on platforms like Upwork:

* Bank statements delivered as PDFs
* Requirement for clean, structured transaction data
* Clear, explainable transformation rules
* Batch processing instead of one-off scripts

The pipeline is designed to be **extendable** to other banks and statement layouts.

---

## Notes

* All data is **synthetic and for demonstration only**
* No real financial accounts are involved
* This demo focuses on **data extraction and normalization**, not financial advice or analysis
