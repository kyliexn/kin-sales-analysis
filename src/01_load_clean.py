"""
01 — Load & Clean Square POS exports.

Inputs:
    2024_Sales__Itemized_.xlsx
    2025_Sales__Itemized_.xlsx

Output:
    outputs/cleaned_sales.csv

The Square "Item Sales Summary" export can contain multiple rows for the
same item when its category assignment changes during a year. We aggregate
those rows to one item-year record before performing comparisons.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


NUMERIC_COLUMNS = [
    "Items Sold",
    "Gross Sales",
    "Items Refunded",
    "Refunds",
    "Discounts & Comps",
    "Net Sales",
    "Units Sold",
    "Units Refunded",
]


def load_year(path: Path, year: int) -> pd.DataFrame:
    df = pd.read_excel(path)
    df["Year"] = year
    return df


def clean_sales(input_dir: Path) -> pd.DataFrame:
    files = list(input_dir.glob("*.xlsx"))

    file_2024 = next(f for f in files if "2024" in f.name)
    file_2025 = next(f for f in files if "2025" in f.name)

    df24 = load_year(file_2024, 2024)
    df25 = load_year(file_2025, 2025)

    df = pd.concat([df24, df25], ignore_index=True)

    # "Custom Amount" represents ad-hoc charges rather than a menu item.
    df = df.loc[df["Item Name"].ne("Custom Amount")].copy()

    # Normalize category labels before classification.
    df["Category"] = (
        df["Category"]
        .fillna("Unknown")
        .astype(str)
        .str.strip()
        .str.title()
    )

    # Make sure expected numeric fields are numeric.
    for col in NUMERIC_COLUMNS:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    missing = [col for col in NUMERIC_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(f"Missing expected columns: {missing}")

    # If Square split an item across categories, use the category with the
    # largest Net Sales as the representative category for that item-year.
    category_lookup = (
        df.sort_values("Net Sales", ascending=False)
        .drop_duplicates(["Item Name", "Year"])
        [["Item Name", "Year", "Category"]]
    )

    aggregated = (
        df.groupby(["Item Name", "Year"], as_index=False)[NUMERIC_COLUMNS]
        .sum()
        .merge(category_lookup, on=["Item Name", "Year"], how="left")
    )

    return aggregated


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", type=Path, default=Path("."))
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    cleaned = clean_sales(args.input_dir)

    output = args.output_dir / "cleaned_sales.csv"
    cleaned.to_csv(output, index=False)

    print(f"Rows after cleaning/aggregation: {len(cleaned):,}")
    print(f"Saved: {output}")


if __name__ == "__main__":
    main()
