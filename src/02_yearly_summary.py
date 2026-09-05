"""
02 — Overall yearly summary.

Input:
    outputs/cleaned_sales.csv

Output:
    outputs/yearly_summary.csv
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


def build_summary(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)

    yearly = (
        df.groupby("Year")
        .agg(
            total_net_sales=("Net Sales", "sum"),
            total_units_sold=("Units Sold", "sum"),
            unique_items=("Item Name", "nunique"),
            total_discounts=("Discounts & Comps", "sum"),
            total_refunds=("Refunds", "sum"),
        )
        .sort_index()
    )

    yearly["net_sales_per_unit"] = (
        yearly["total_net_sales"] / yearly["total_units_sold"]
    ).where(yearly["total_units_sold"].ne(0))

    if {2024, 2025}.issubset(yearly.index):
        yearly["net_sales_yoy_pct"] = (
            yearly["total_net_sales"].pct_change() * 100
        )
        yearly["units_yoy_pct"] = (
            yearly["total_units_sold"].pct_change() * 100
        )

    return yearly.round(2)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()

    path = args.output_dir / "cleaned_sales.csv"
    yearly = build_summary(path)

    output = args.output_dir / "yearly_summary.csv"
    yearly.to_csv(output)

    print("\nOVERALL YEARLY SUMMARY")
    print(yearly.to_string())
    print(f"\nSaved: {output}")


if __name__ == "__main__":
    main()
