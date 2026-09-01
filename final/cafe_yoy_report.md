# Cafe Sales: 2024 vs 2025 Year-over-Year Analysis

## Data & Method

Source: Square's Item Sales Summary export for 2024 and 2025 (one row per item per year).
No timestamps are included in this export, so this analysis covers year-over-year item
performance.

**Cleaning notes:**
- Removed the "Custom Amount" line (manual charges).
- Square splits an item into multiple rows if it was recategorized mid-year. These were
  collapsed back into one row per item per year, keeping the category with the larger sales
  share as the item's "main" category for that year.

Not every item on the menu is a fixed, ongoing product:

| Type | Rotation | Example |
|---|---|---|
| Permanent drinks (16 total) | Always available | Matcha Latte, Vietnamese Iced Coffee |
| Mochi Donuts | Flavors rotate weekly, except Cinnamon Sugar (fixed) | this week's flavor |
| GF Mochi Muffins | Flavors rotate daily (Black Sesame/Chocolate/Ube/Pandan) | today's flavor |
| Brioche Donuts | Weekend-only, flavors rotate | this weekend's flavor |

This analysis splits into permanent items (compared item-by-item) and rotating groups 
(compared as a total category), as comparing each item individually would give 
permanent menu items a much higher leverage.

---

## 1. Overall Growth

| Metric | 2024 | 2025 | Change |
|---|---|---|---|
| Net Sales | $1,027,752 | $1,330,895 | **+29.5%** |
| Units Sold | 227,321 | 264,334 | **+16.3%** |
| Avg. price per unit | $4.52 | $5.03 | +11.3% |

Revenue grew faster than unit volume, meaning average spend per item sold went up. This implies a 
mix of price increases in combination with a shift toward higher-priced items

![Total sales YoY](charts/01_total_sales_yoy.png)

## 2. Permanent Menu Items — the fair comparison

These 16 drinks (plus the one fixed mochi donut flavor, Cinnamon Sugar) are on the menu every
day of both years, so this is the most direct comparison we can perform on what's winning and losing:

![Permanent items YoY](charts/02_permanent_items_yoy.png)

- **Growing the most:** Matcha Strawberry (+147%, +$59.6K), Matcha Einspanner (+63%, +$55.8K),
  Cinnamon Sugar Mochi Donut (+104%, +$29.6K), Matcha Latte (+78%, +$14.5K). Matcha is clearly
  the standout flavor trend across the permanent lineup.
- **Declining:** Ssuk/Mugwort Cream Top (-34%), Jasmine Oat Latte (-13%), Black Sesame Cream
  Top (-2%), Cream Top (-11%). The Ssuk is worth noting, as it lost a third of its sales.

## 3. Rotating Categories — compared as a whole

Since individual flavors rotate, the fair comparison here is total category revenue:

![Rotating categories YoY](charts/03_rotating_categories_yoy.png)

- Brioche Donuts fell 65% ($92K → $32K). Was this a weekend availability cut, did fewer flavors get made, or demand drop?
- GF Muffins grew 56% ($42K → $66K)
- Mochi Donuts were essentially flat (+5%, $352K → $369K)

## 4. Which flavors perform best when offered

Not a trend metric (since not every flavor was offered in both years) — this just shows which
flavors earn the most on the days/weeks they're in rotation, useful for deciding what to bring
back more often:

![Flavor popularity](charts/04_flavor_popularity.png)

Dubai Chocolate and Cinnamon Sugar lead mochi donuts; Ube is the runaway leader among
GF muffins (far ahead of the next flavor); Mango Sticky Rice and Tiramisu lead brioche donuts.

---

## Takeaways

1. 29.5% revenue growth with only 16.3% more units sold means each sale is worth more on average now than a year ago.
2. The Strawberry Matcha, Matcha Einspanner, and Matcha Latte are the most profitable and popular items.
3. Brioche Donuts are down sharply (-65%) as a category.
4. Mochi Donuts seem to plateau year-over-year, meaning growth is coming mainly from drinks.
5. Ube serves as the most popular GF mochi muffin flavor by far, which could potentially help with profits
   the more often it is introduced in the weekly rotation.

---
