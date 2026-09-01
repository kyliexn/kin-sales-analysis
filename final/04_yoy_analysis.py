"""
04: Year-over-Year Comparison (Corrected)
============================================
Two different kinds of comparison, matched to what's actually fair:

A) PERMANENT items (16 drinks + Cinnamon Sugar donut): compare individual
   item $ YoY -- a fair, apples-to-apples comparison.

B) ROTATING groups (Mochi Donut flavors, GF Muffin flavors, Brioche Donut
   flavors): compare TOTAL CATEGORY $ YoY, since an individual flavor's $
   mostly reflects how many days/weeks it happened to be offered, not
   real demand. We also rank flavor popularity (avg $ when offered) as a
   separate, non-trend view.

Input:  classified_sales.csv
Output: permanent_items_yoy.csv, rotating_categories_yoy.csv,
        flavor_popularity.csv
"""
import pandas as pd

df = pd.read_csv("classified_sales.csv")

# =================================================================
# A) PERMANENT ITEMS -- fair YoY comparison
# =================================================================
permanent = df[df["menu_type"].isin(["Permanent Drink", "Permanent Donut"])]

perm_pivot = permanent.pivot_table(
    index="display_name", columns="Year", values="Net Sales", aggfunc="sum"
)
perm_pivot["dollar_change"] = perm_pivot[2025] - perm_pivot[2024]
perm_pivot["pct_change"] = (perm_pivot["dollar_change"] / perm_pivot[2024] * 100).round(1)
perm_pivot = perm_pivot.sort_values("dollar_change", ascending=False)

print("=" * 60)
print("A) PERMANENT ITEMS -- YoY change (fair comparison)")
print("=" * 60)
print(perm_pivot.round(1))
perm_pivot.to_csv("permanent_items_yoy.csv")

# =================================================================
# B) ROTATING GROUPS -- category-level YoY
# =================================================================
rotating = df[df["menu_type"].str.startswith("Rotating", na=False)]

cat_pivot = rotating.pivot_table(
    index="menu_type", columns="Year", values="Net Sales", aggfunc="sum"
)
cat_pivot["dollar_change"] = cat_pivot[2025] - cat_pivot[2024]
cat_pivot["pct_change"] = (cat_pivot["dollar_change"] / cat_pivot[2024] * 100).round(1)

print(f"\n{'=' * 60}")
print("B) ROTATING CATEGORIES -- total $ YoY")
print("=" * 60)
print(cat_pivot.round(1))
cat_pivot.to_csv("rotating_categories_yoy.csv")

# ---- Flavor popularity within each rotating group (NOT a trend metric) ----
print(f"\n{'=' * 60}")
print("FLAVOR POPULARITY (combined 2024+2025 $, when offered)")
print("=" * 60)

for group in ["Rotating: Mochi Donut Flavor", "Rotating: GF Muffin Flavor", "Rotating: Brioche Donut Flavor"]:
    sub = rotating[rotating["menu_type"] == group]
    flavor_totals = sub.groupby("Item Name")["Net Sales"].sum().sort_values(ascending=False)
    print(f"\n--- {group} (top 10 of {len(flavor_totals)}) ---")
    print(flavor_totals.head(10).round(0))

rotating.groupby(["menu_type", "Item Name"])["Net Sales"].sum().reset_index().to_csv(
    "flavor_popularity.csv", index=False
)
print("\nSaved -> permanent_items_yoy.csv, rotating_categories_yoy.csv, flavor_popularity.csv")
