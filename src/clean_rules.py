# src/clean_rules.py

import pandas as pd

from src.config import (
    FINAL_COLUMNS,
    RAW_DEBIT_COLUMN,
    RAW_CREDIT_COLUMN,
    RAW_NUMERIC_COLUMNS,
    NON_TRANSACTION_DESCRIPTIONS,
    DEBIT_SIGN,
    CREDIT_SIGN,
    AMOUNT_COLUMN,
)


def drop_non_transaction_rows(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove rows that are not actual transactions
    (e.g. Opening Balance).
    """
    mask = ~df["description"].str.lower().isin(NON_TRANSACTION_DESCRIPTIONS)
    return df.loc[mask].reset_index(drop=True)


def parse_amount(df: pd.DataFrame) -> pd.DataFrame:
    """
    Combine debit / credit columns into a single signed amount.
    Debit  -> negative
    Credit -> positive
    """
    def _row_amount(row):
        if pd.notna(row[RAW_DEBIT_COLUMN]) and row[RAW_DEBIT_COLUMN] != "":
            return DEBIT_SIGN * float(row[RAW_DEBIT_COLUMN])
        if pd.notna(row[RAW_CREDIT_COLUMN]) and row[RAW_CREDIT_COLUMN] != "":
            return CREDIT_SIGN * float(row[RAW_CREDIT_COLUMN])
        return 0.0

    df[AMOUNT_COLUMN] = df.apply(_row_amount, axis=1)
    return df


def to_numeric(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert numeric columns from string to float.
    Safely handles missing values.
    """
    for col in RAW_NUMERIC_COLUMNS:
        if col in df.columns:
            df[col] = (
                df[col]
                .astype(str)
                .str.replace(",", "", regex=False)
                .replace("", pd.NA)
            )
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


def finalize_schema(df: pd.DataFrame) -> pd.DataFrame:
    """
    Select final columns and enforce column order.
    """
    return df[FINAL_COLUMNS].copy()
