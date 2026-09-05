"""
05 — Generate portfolio-ready charts.

Inputs:
    outputs/yearly_summary.csv
    outputs/permanent_items_yoy.csv
    outputs/rotating_categories_yoy.csv
    outputs/flavor_popularity.csv
    outputs/revenue_concentration.csv

Outputs:
    charts/*.png
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import pandas as pd


def currency_axis(ax) -> None:
    ax.yaxis.set_major_formatter(
        mticker.FuncFormatter(lambda x, _: f"${x:,.0f}")
    )


def save_total_sales(yearly: pd.DataFrame, charts_dir: Path) -> None:
    fig, ax = plt.subplots(figsize=(7, 5))
    years = yearly.index.astype(str)
    bars = ax.bar(years, yearly["total_net_sales"])

    ax.set_title("Kin Bakeshop Net Sales by Year")
    ax.set_ylabel("Net Sales")
    currency_axis(ax)

    for bar, value in zip(bars, yearly["total_net_sales"]):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            value,
            f"${value:,.0f}",
            ha="center",
            va="bottom",
        )

    if {2024, 2025}.issubset(yearly.index):
        pct = (
            yearly.loc[2025, "total_net_sales"]
            / yearly.loc[2024, "total_net_sales"]
            - 1
        ) * 100
        ax.text(
            0.5,
            0.92,
            f"{pct:+.1f}% YoY",
            transform=ax.transAxes,
            ha="center",
            fontweight="bold",
        )

    fig.tight_layout()
    fig.savefig(charts_dir / "01_total_sales_yoy.png", dpi=180)
    plt.close(fig)


def save_permanent_yoy(perm: pd.DataFrame, charts_dir: Path) -> None:
    data = perm.sort_values("dollar_change")

    fig, ax = plt.subplots(figsize=(9, 8))
    ax.barh(data.index, data["dollar_change"])
    ax.axvline(0, linewidth=0.8)

    ax.set_title("Permanent Menu Items: Net Sales Change, 2024 → 2025")
    ax.set_xlabel("Change in Net Sales")
    ax.xaxis.set_major_formatter(
        mticker.FuncFormatter(lambda x, _: f"${x:,.0f}")
    )

    fig.tight_layout()
    fig.savefig(charts_dir / "02_permanent_items_yoy.png", dpi=180)
    plt.close(fig)


def save_rotating_categories(cat: pd.DataFrame, charts_dir: Path) -> None:
    labels = [
        i.replace("Rotating: ", "").replace(" Flavor", "")
        for i in cat.index
    ]

    fig, ax = plt.subplots(figsize=(8, 5.5))
    x = range(len(cat))

    width = 0.38
    ax.bar([i - width / 2 for i in x], cat["2024"], width, label="2024")
    ax.bar([i + width / 2 for i in x], cat["2025"], width, label="2025")

    ax.set_xticks(list(x))
    ax.set_xticklabels(labels)
    ax.set_ylabel("Net Sales")
    ax.set_title("Rotating Product Categories: Net Sales by Year")
    currency_axis(ax)
    ax.legend()

    fig.tight_layout()
    fig.savefig(charts_dir / "03_rotating_categories_yoy.png", dpi=180)
    plt.close(fig)


def save_flavors(flavors: pd.DataFrame, charts_dir: Path) -> None:
    groups = flavors["menu_type"].drop_duplicates().tolist()

    fig, axes = plt.subplots(
        nrows=len(groups),
        ncols=1,
        figsize=(9, max(4, 3.5 * len(groups))),
    )
    if len(groups) == 1:
        axes = [axes]

    for ax, group in zip(axes, groups):
        data = (
            flavors[flavors["menu_type"].eq(group)]
            .nlargest(8, "Net Sales")
            .sort_values("Net Sales")
        )

        labels = (
            data["Item Name"]
            .str.replace(r"^(MD: |BD: |GFM: )", "", regex=True)
        )

        ax.barh(labels, data["Net Sales"])
        ax.set_title(group.replace("Rotating: ", ""))
        ax.xaxis.set_major_formatter(
            mticker.FuncFormatter(lambda x, _: f"${x:,.0f}")
        )

    fig.suptitle(
        "Top Rotating Flavors by Combined 2024–2025 Revenue",
        fontweight="bold",
    )
    fig.tight_layout()
    fig.savefig(
        charts_dir / "04_flavor_popularity.png",
        dpi=180,
        bbox_inches="tight",
    )
    plt.close(fig)


def save_concentration(concentration: pd.DataFrame, charts_dir: Path) -> None:
    data = concentration.head(15).copy()

    fig, ax = plt.subplots(figsize=(9, 6))
    ax.bar(data["Item Name"], data["revenue_share"] * 100)
    ax.set_ylabel("Share of Total Revenue (%)")
    ax.set_title("Revenue Concentration: Top 15 Products")
    ax.tick_params(axis="x", rotation=75)

    fig.tight_layout()
    fig.savefig(charts_dir / "05_revenue_concentration.png", dpi=180)
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    parser.add_argument("--charts-dir", type=Path, default=Path("charts"))
    args = parser.parse_args()

    args.charts_dir.mkdir(parents=True, exist_ok=True)

    yearly = pd.read_csv(args.output_dir / "yearly_summary.csv", index_col="Year")
    perm = pd.read_csv(
        args.output_dir / "permanent_items_yoy.csv",
        index_col="display_name",
    )
    cat = pd.read_csv(
        args.output_dir / "rotating_categories_yoy.csv",
        index_col="menu_type",
    )
    flavors = pd.read_csv(args.output_dir / "flavor_popularity.csv")
    concentration = pd.read_csv(
        args.output_dir / "revenue_concentration.csv"
    )

    save_total_sales(yearly, args.charts_dir)
    save_permanent_yoy(perm, args.charts_dir)
    save_rotating_categories(cat, args.charts_dir)
    save_flavors(flavors, args.charts_dir)
    save_concentration(concentration, args.charts_dir)

    print(f"Charts saved to: {args.charts_dir}")


if __name__ == "__main__":
    main()
