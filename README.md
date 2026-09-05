# Kin Bakeshop Sales Analytics

### 2024–2025 Year-over-Year Sales & Menu Performance

**Python · Pandas · Matplotlib · Exploratory Data Analysis · Business Analytics**

## Overview

This project analyzes two years of Square point-of-sale data from Kin Bakeshop to evaluate changes in sales performance between 2024 and 2025.

The analysis focuses on:

- Overall revenue and unit growth
- Permanent menu-item performance
- Rotating baked-good categories
- Rotating flavor performance
- Revenue concentration across products

### The analytical challenge

Not every product can be compared directly year-over-year.

Kin's mochi donuts rotate weekly, GF mochi muffins rotate daily, and brioche donuts rotate on a weekend schedule. An individual flavor's annual revenue therefore depends not only on customer demand, but also on how frequently that flavor was offered.

To avoid misleading comparisons, this project separates **permanent** products from **rotating** products:

- Permanent products → item-level YoY comparison
- Rotating products → category-level YoY comparison
- Rotating flavors → descriptive ranking by combined revenue, not a demand-trend claim

---

## Business Questions

1. How did Kin Bakeshop's overall sales performance change from 2024 to 2025?
2. Which permanent menu items contributed most to revenue growth or decline?
3. How did rotating product categories perform year-over-year?
4. Which rotating flavors generated the most revenue?
5. How concentrated was revenue among the highest-selling products?

---

## Key Findings

From the current analysis:

- Net sales increased from **$1.03M in 2024 to $1.33M in 2025 (+29.5%)**.
- Units sold increased from **227K to 264K (+16.3%)**.
- Net sales per unit increased from **$4.52 to $5.03 (+11.3%)**.
- Among permanent products, **Matcha Strawberry** and **Matcha Einspanner** were the largest dollar-growth contributors.
- **Brioche Donuts declined 65%** at the category level, while **GF Muffins increased 56%**.
- **Mochi Donuts increased approximately 5%**, making the category broadly stable year-over-year.

> Important: "net sales per unit" is not the same as average customer transaction value because the available dataset is an item-level sales summary rather than a customer-level transaction dataset.

---

## Methodology

### 1. Data cleaning

The pipeline:

- Loads the 2024 and 2025 Square exports
- Adds a year identifier
- Removes the non-menu `Custom Amount` row
- Standardizes category labels
- Converts expected numeric fields to numeric values
- Collapses Square's split category rows back to one item-year record
- Assigns the category with the largest net sales share as the representative category

### 2. Menu classification

Products are classified using the cafe's actual menu structure.

| Menu type | Comparison |
|---|---|
| Permanent drinks | Item-level YoY |
| Cinnamon Sugar mochi donut | Item-level YoY |
| Rotating mochi donuts | Category-level YoY |
| Rotating GF muffins | Category-level YoY |
| Rotating brioche donuts | Category-level YoY |
| Other / seasonal | Excluded from core YoY comparisons |

### 3. Year-over-year analysis

Permanent items are compared directly between 2024 and 2025.

Rotating categories are aggregated before comparison so that changes in the rotation schedule are not automatically interpreted as changes in product demand.

### 4. Revenue concentration

The pipeline also calculates each product's share of total revenue and cumulative revenue share, enabling a Pareto-style view of how concentrated sales are among top products.

---

## Project Structure

```text
kin-bakeshop-sales-analytics/
├── data/
│   └── README.md
├── src/
│   ├── 01_load_clean.py
│   ├── 02_yearly_summary.py
│   ├── 03_classify_menu.py
│   ├── 04_yoy_analysis.py
│   └── 05_charts.py
├── charts/
├── outputs/
├── run_analysis.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Reproduce the Analysis

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Add the raw Square exports

Place:

```text
data/2024_Sales__Itemized_.xlsx
data/2025_Sales__Itemized_.xlsx
```

inside the `data/` folder.

### 3. Run the complete pipeline

```bash
python run_analysis.py
```

The pipeline creates:

```text
outputs/
├── cleaned_sales.csv
├── yearly_summary.csv
├── classified_sales.csv
├── permanent_items_yoy.csv
├── rotating_categories_yoy.csv
├── flavor_popularity.csv
└── revenue_concentration.csv
```

and:

```text
charts/
├── 01_total_sales_yoy.png
├── 02_permanent_items_yoy.png
├── 03_rotating_categories_yoy.png
├── 04_flavor_popularity.png
└── 05_revenue_concentration.png
```

---

## Limitations

The source data is an item-level Square sales summary rather than a transaction-level dataset.

Therefore, this project cannot directly measure:

- Customer-level average order value
- Customer retention
- Number of unique customers
- Daily/weekly sales seasonality
- Exact number of days each rotating flavor was offered

Because rotating flavors were not observed with consistent exposure periods, their combined annual revenue should not be interpreted as a pure measure of customer preference.

---

## Future Improvements

Potential extensions include:

- Adding transaction-level data for customer and order analysis
- Normalizing rotating-flavor performance by days/weeks offered
- Adding monthly or weekly seasonality analysis when date-level data is available
- Building a Tableau or Power BI dashboard
- Testing whether observed YoY changes are statistically significant
- Adding sales forecasting

---

## Tools

- Python
- Pandas
- Matplotlib
- Excel / Square POS exports
- Exploratory Data Analysis
- Data Cleaning
- Data Aggregation
- Year-over-Year Analysis
- Business Analytics
