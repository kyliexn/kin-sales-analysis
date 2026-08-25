"""
05: Charts
===========
Builds every chart used in the final report.

Input:  yearly_summary.csv, permanent_items_yoy.csv,
        rotating_categories_yoy.csv, flavor_popularity.csv
Output: charts/*.png
"""
import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.size": 11,
    "axes.spines.top": False,
    "axes.spines.right": False,
})

os.makedirs("charts", exist_ok=True)

COLOR_24 = "#8c8c8c"
COLOR_25 = "#2f6f4f"
COLOR_NEG = "#b23a48"

yearly = pd.read_csv("yearly_summary.csv", index_col="Year")
perm = pd.read_csv("permanent_items_yoy.csv", index_col="display_name")
cat = pd.read_csv("rotating_categories_yoy.csv", index_col="menu_type")
flavors = pd.read_csv("flavor_popularity.csv")

# -----------------------------------------------------------
# Chart 1: Total net sales, 2024 vs 2025
# -----------------------------------------------------------
fig, ax = plt.subplots(figsize=(6, 5))
bars = ax.bar(["2024", "2025"], yearly["total_net_sales"], color=[COLOR_24, COLOR_25], width=0.5)
ax.set_title("Total Net Sales by Year", fontsize=14, fontweight="bold")
ax.set_ylabel("Net Sales ($)")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
for bar, val in zip(bars, yearly["total_net_sales"]):
    ax.text(bar.get_x() + bar.get_width()/2, val + 15000, f"${val:,.0f}",
            ha="center", fontweight="bold")
pct = (yearly.loc[2025, "total_net_sales"] / yearly.loc[2024, "total_net_sales"] - 1) * 100
ax.text(0.5, 0.92, f"+{pct:.0f}% YoY", transform=ax.transAxes, ha="center",
        fontsize=12, color=COLOR_25, fontweight="bold")
plt.tight_layout()
plt.savefig("charts/01_total_sales_yoy.png", dpi=150)
plt.close()

# -----------------------------------------------------------
# Chart 2: All permanent items, YoY $ change (fair comparison)
# -----------------------------------------------------------
perm_sorted = perm.sort_values("dollar_change")
fig, ax = plt.subplots(figsize=(9, 8))
colors = [COLOR_25 if v > 0 else COLOR_NEG for v in perm_sorted["dollar_change"]]
ax.barh(perm_sorted.index, perm_sorted["dollar_change"], color=colors)
ax.axvline(0, color="black", linewidth=0.8)
ax.set_title("Permanent Menu Items: Net Sales Change, 2024 -> 2025\n(fair item-to-item comparison)",
              fontsize=13, fontweight="bold")
ax.set_xlabel("Change in Net Sales ($)")
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
plt.tight_layout()
plt.savefig("charts/02_permanent_items_yoy.png", dpi=150)
plt.close()

# -----------------------------------------------------------
# Chart 3: Rotating categories, total $ YoY
# -----------------------------------------------------------
fig, ax = plt.subplots(figsize=(8, 5.5))
labels = [i.replace("Rotating: ", "").replace(" Flavor", "") for i in cat.index]
x = range(len(cat))
ax.bar([i - 0.2 for i in x], cat["2024"], width=0.4, label="2024", color=COLOR_24)
ax.bar([i + 0.2 for i in x], cat["2025"], width=0.4, label="2025", color=COLOR_25)
ax.set_xticks(list(x))
ax.set_xticklabels(labels, fontsize=10)
ax.set_ylabel("Total Net Sales ($)")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
ax.set_title("Rotating Categories: Total Net Sales YoY\n(all flavors combined)", fontsize=13, fontweight="bold")
for i, (v24, v25) in enumerate(zip(cat["2024"], cat["2025"])):
    pct_i = (v25 - v24) / v24 * 100
    color = COLOR_25 if pct_i > 0 else COLOR_NEG
    ax.text(i, max(v24, v25) + 15000, f"{pct_i:+.0f}%", ha="center", fontweight="bold", color=color)
ax.legend()
plt.tight_layout()
plt.savefig("charts/03_rotating_categories_yoy.png", dpi=150)
plt.close()

# -----------------------------------------------------------
# Chart 4: Top flavors per rotating group (popularity, not trend)
# -----------------------------------------------------------
fig, axes = plt.subplots(1, 3, figsize=(15, 6))
groups = ["Rotating: Mochi Donut Flavor", "Rotating: GF Muffin Flavor", "Rotating: Brioche Donut Flavor"]
titles = ["Mochi Donut Flavors\n(top 8 by total $)", "GF Muffin Flavors\n(all flavors)", "Brioche Donut Flavors\n(top 8 by total $)"]

for ax, group, title in zip(axes, groups, titles):
    sub = flavors[flavors["menu_type"] == group].sort_values("Net Sales", ascending=False).head(8)
    sub = sub.sort_values("Net Sales")
    labels = sub["Item Name"].str.replace("MD: ", "").str.replace("BD: ", "").str.replace("GFM: ", "")
    ax.barh(labels, sub["Net Sales"], color=COLOR_25)
    ax.set_title(title, fontsize=11, fontweight="bold")
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
    ax.tick_params(axis="y", labelsize=9)

fig.suptitle("Best-Selling Flavors When Offered (2024+2025 combined)", fontsize=14, fontweight="bold", y=1.02)
plt.tight_layout()
plt.savefig("charts/04_flavor_popularity.png", dpi=150, bbox_inches="tight")
plt.close()

print("All charts saved to charts/")
for f in sorted(os.listdir("charts")):
    print(" -", f)
