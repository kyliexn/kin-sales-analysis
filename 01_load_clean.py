"""
01: Load & Clean
=================
Square's "Item Sales Summary" export gives one row per item PER CATEGORY
ASSIGNMENT PERIOD -- meaning if an item got recategorized partway through
the year (e.g. moved from "Uncategorized" into "Brioche Donuts"), Square
splits it into two rows. We collapse those back into one row per item
per year before comparing 2024 vs 2025.

Input:  the two raw Square exports
Output: cleaned_sales.csv (one row per item per year)
"""
import pandas as pd

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 200)

# ---- Load both years ----
df24 = pd.read_excel("2024_Sales__Itemized_.xlsx")
df25 = pd.read_excel("2025_Sales__Itemized_.xlsx")

df24["Year"] = 2024
df25["Year"] = 2025

df = pd.concat([df24, df25], ignore_index=True)

# ---- Drop the non-item "Custom Amount" row ----
# Represents ad-hoc manual charges, not an actual menu item.
df = df[df["Item Name"] != "Custom Amount"].copy()

# ---- Clean category text ----
# Categories have inconsistent casing/spacing across years
# (e.g. "GF mochi donuts" vs "GF Mochi Donuts").
df["Category"] = df["Category"].str.strip().str.title()

# ---- Collapse split rows: one row per Item Name per Year ----
numeric_cols = [
    "Items Sold", "Gross Sales", "Items Refunded", "Refunds",
    "Discounts & Comps", "Net Sales", "Units Sold", "Units Refunded",
]

# Category with the most Net Sales wins as the "representative" category
cat_lookup = (
    df.sort_values("Net Sales", ascending=False)
    .drop_duplicates(subset=["Item Name", "Year"])[["Item Name", "Year", "Category"]]
)

agg = df.groupby(["Item Name", "Year"], as_index=False)[numeric_cols].sum()
agg = agg.merge(cat_lookup, on=["Item Name", "Year"], how="left")

print(f"Rows before collapsing: {len(df)}")
print(f"Rows after collapsing:  {len(agg)}")

agg.to_csv("cleaned_sales.csv", index=False)
print("Saved -> cleaned_sales.csv")
