"""
03 — Classify products by menu structure.

Permanent products are appropriate for item-level YoY comparisons.
Rotating products are compared at the category level because a flavor's
annual revenue depends heavily on how often it was offered.

Input:
    outputs/cleaned_sales.csv

Output:
    outputs/classified_sales.csv
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


# Internal/owner-facing names mapped to the corresponding Square item names.
PERMANENT_DRINKS = {
    "Einspanner: Espresso": "Einspanner",
    "Black Sesame Cream Top": "Black Sesame Cream Top",
    "Cream Top": "Cream Top",
    "Vietnamese Iced Coffee": "Vietnamese Coffee",
    "Jasmine Oat Latte": "Jasmine Oat Latte",
    "Einspanner: Matcha": "Matcha Einspanner",
    "Einspanner: Hojicha": "Hojicha Einspanner",
    "Matcha Strawberry": "Strawberry Matcha Latte",
    "Hojicha Strawberry": "Strawberry Hojicha Latte",
    "Matcha Black Sesame": "Matcha Black Sesame Cream Top",
    "Hojicha Black Sesame": "Hojicha Black Sesame Cream Top",
    "Latte: Matcha": "Matcha Latte",
    "Latte: Hojicha": "Hojicha Latte",
    "Thai Tea Cream Top": "Thai Tea Cream Top",
    "Sook Cream Top": "Ssuk (Mugwort)",
    "Strawberry Milk": "Strawberry Milk",
}

PERMANENT_DONUTS = {"MD: Cinnamon Sugar"}

ROTATING_CATEGORIES = {
    "Mochi Donuts": "Rotating: Mochi Donut Flavor",
    "Gf Mochi Muffins": "Rotating: GF Muffin Flavor",
    "Brioche Donuts": "Rotating: Brioche Donut Flavor",
}


def classify(row: pd.Series) -> str:
    if row["Item Name"] in PERMANENT_DRINKS:
        return "Permanent Drink"

    if row["Item Name"] in PERMANENT_DONUTS:
        return "Permanent Donut"

    if row["Category"] in ROTATING_CATEGORIES:
        return ROTATING_CATEGORIES[row["Category"]]

    return "Other / Seasonal"


def classify_menu(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    df["menu_type"] = df.apply(classify, axis=1)

    reverse_map = {square: display for display, square in PERMANENT_DRINKS.items()}
    df["display_name"] = (
        df["Item Name"].map(reverse_map).fillna(df["Item Name"])
    )

    return df


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()

    path = args.output_dir / "cleaned_sales.csv"
    classified = classify_menu(path)

    output = args.output_dir / "classified_sales.csv"
    classified.to_csv(output, index=False)

    print("\nRevenue by menu type:")
    print(
        classified.groupby("menu_type")["Net Sales"]
        .sum()
        .sort_values(ascending=False)
        .round(0)
        .to_string()
    )
    print(f"\nSaved: {output}")


if __name__ == "__main__":
    main()
