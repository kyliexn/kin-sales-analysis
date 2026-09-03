# Cafe Sales Analysis: 2024 vs 2025

## Start here
**`cafe_yoy_report.md`** — the full write-up with charts and takeaways.

## Files

| File | What it is |
|---|---|
| `cafe_yoy_report.md` | Final report |
| `charts/` | All 4 charts referenced in the report |
| `01_load_clean.py` → `05_charts.py` | Analysis pipeline |
| `cleaned_sales.csv` | Both years combined, one row per item per year |
| `classified_sales.csv` | Same, plus a `menu_type` column (permanent vs. rotating) |
| `permanent_items_yoy.csv` | The 16 fixed drinks + Cinnamon Sugar donut, 2024 vs 2025 |
| `rotating_categories_yoy.csv` | Mochi Donuts / GF Muffins / Brioche Donuts totals, 2024 vs 2025 |
| `flavor_popularity.csv` | Every rotating flavor ever sold, ranked by total $ |
| `yearly_summary.csv` | Overall totals by year |

## Re-running it yourself
Drop the original `2024_Sales__Itemized_.xlsx` and `2025_Sales__Itemized_.xlsx` files in this
same folder and run the scripts in order:

```
python3 01_load_clean.py
python3 02_yearly_summary.py
python3 03_classify_menu.py
python3 04_yoy_analysis.py
python3 05_charts.py
```

Each script prints its results and saves a CSV (or PNGs, for the last one) that the next
script reads in.

## Why "permanent vs. rotating" matters
Mochi Donut and Brioche Donut flavors rotate on a weekly basis, and GF Muffins
rotate daily. Comparing one flavor's 2024 sales to its 2025 sales mostly reflects how many
weeks/days it happened to be offered instead of real demand change. `03_classify_menu.py` splits
items into "permanent" (fair to compare individually) and "rotating" (only fair to compare as
a category total) before any YoY math happens.
