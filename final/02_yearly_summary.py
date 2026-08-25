"""
02: Overall Yearly Summary
============================
The big-picture question: did the cafe grow from 2024 to 2025?
This comparison is always fair since it's just total revenue, no
item-level assumptions involved.

Input:  cleaned_sales.csv
Output: yearly_summary.csv
"""
import pandas as pd

df = pd.read_csv("cleaned_sales.csv")

yearly = df.groupby("Year").agg(
    total_net_sales=("Net Sales", "sum"),
    total_units_sold=("Units Sold", "sum"),
    total_items_offered=("Item Name", "nunique"),
    total_discounts=("Discounts & Comps", "sum"),
    total_refunds=("Refunds", "sum"),
).round(2)

yearly["avg_price_per_unit"] = (yearly["total_net_sales"] / yearly["total_units_sold"]).round(2)

print("=" * 60)
print("OVERALL YEAR-OVER-YEAR SUMMARY")
print("=" * 60)
print(yearly)

pct_change = (
    (yearly.loc[2025, "total_net_sales"] - yearly.loc[2024, "total_net_sales"])
    / yearly.loc[2024, "total_net_sales"] * 100
)
unit_change = (
    (yearly.loc[2025, "total_units_sold"] - yearly.loc[2024, "total_units_sold"])
    / yearly.loc[2024, "total_units_sold"] * 100
)
print(f"\nNet sales change 2024 -> 2025: {pct_change:+.1f}%")
print(f"Units sold change 2024 -> 2025: {unit_change:+.1f}%")

yearly.to_csv("yearly_summary.csv")
print("\nSaved -> yearly_summary.csv")
