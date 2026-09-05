"""
04 — Year-over-year analysis.

Permanent products:
    Compare individual items across 2024 and 2025.

Rotating products:
    Compare total category revenue across years.

Flavor performance:
    Rank flavors by combined 2024–2025 revenue. This is a sales-volume
    description, NOT a year-over-year demand metric, because annual revenue
    is affected by how frequently each flavor was offered.

Inputs:
    outputs/classified_sales.csv

Outputs:
    outputs/permanent_items_yoy.csv
    outputs/rotating_categories_yoy.csv
    outputs/flavor_popularity.csv
    outputs/revenue_concentration.csv
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


PERMANENT_TYPES = ["Permanent Drink", "Permanent Donut"]


def yoy_table(df: pd.DataFrame, index_col: str) -> pd.DataFrame:
    pivot = df.pivot_table(
        index=index_col,
        columns="Year",
        values="Net Sales",
        aggfunc="sum",
        fill_value=0,
    )

    for year in [2024, 2025]:
        if year not in pivot.columns:
            pivot[year] = 0

    pivot["dollar_change"] = pivot[2025] - pivot[2024]
    pivot["pct_change"] = (
        pivot["dollar_change"]
        .div(pivot[2024].replace(0, pd.NA))
        .mul(100)
    )

    return pivot.sort_values("dollar_change", ascending=False).round(2)


def build_analyses(path: Path, output_dir: Path) -> None:
    df = pd.read_csv(path)

    permanent = df[df["menu_type"].isin(PERMANENT_TYPES)].copy()
    permanent_yoy = yoy_table(permanent, "display_name")
    permanent_yoy.to_csv(output_dir / "permanent_items_yoy.csv")

    rotating = df[df["menu_type"].str.startswith("Rotating", na=False)].copy()
    rotating_yoy = yoy_table(rotating, "menu_type")
    rotating_yoy.to_csv(output_dir / "rotating_categories_yoy.csv")

    flavor = (
        rotating.groupby(["menu_type", "Item Name"], as_index=False)["Net Sales"]
        .sum()
        .sort_values(["menu_type", "Net Sales"], ascending=[True, False])
    )
    flavor.to_csv(output_dir / "flavor_popularity.csv", index=False)

    # Pareto-style revenue concentration: what share of total revenue comes
    # from the highest-selling products?
    product_revenue = (
        df.groupby("Item Name", as_index=False)["Net Sales"]
        .sum()
        .sort_values("Net Sales", ascending=False)
    )
    product_revenue["revenue_share"] = (
        product_revenue["Net Sales"] / product_revenue["Net Sales"].sum()
    )
    product_revenue["cumulative_revenue_share"] = (
        product_revenue["revenue_share"].cumsum()
    )
    product_revenue.to_csv(output_dir / "revenue_concentration.csv", index=False)

    print("\nPermanent item YoY:")
    print(permanent_yoy.to_string())

    print("\nRotating category YoY:")
    print(rotating_yoy.to_string())

    print("\nSaved analysis outputs to:", output_dir)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()

    build_analyses(
        args.output_dir / "classified_sales.csv",
        args.output_dir,
    )


if __name__ == "__main__":
    main()
