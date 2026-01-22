# src/config.py

# Final output schema

FINAL_COLUMNS = [
    "date",
    "description",
    "amount",
    "balance",
    "source_file",
]


# Raw extracted columns

RAW_DEBIT_COLUMN = "debit"
RAW_CREDIT_COLUMN = "credit"

RAW_NUMERIC_COLUMNS = [
    "debit",
    "credit",
    "balance",
]

RAW_DATE_COLUMN = "date"


# Cleaning rules

# Rows with these descriptions are NOT transactions
NON_TRANSACTION_DESCRIPTIONS = {
    "opening balance",
}

# Amount sign convention:
# - debit  → negative
# - credit → positive
DEBIT_SIGN = -1
CREDIT_SIGN = 1


# Date parsing


DATE_FORMATS = [
    "%m/%d/%Y",
    "%d/%m/%Y",
]


# Output

AMOUNT_COLUMN = "amount"
