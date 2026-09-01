"""
03: Classify Items by Menu Structure
=======================================
Not all items are directly comparable year-over-year. Many "flavors" are
rotating slots within a fixed menu structure, so an individual flavor's
$ change reflects HOW OFTEN it was in rotation, not real demand trend.

Menu structure (from the cafe's actual operations, not visible in the
POS data itself):
- Mochi Donuts: flavors rotate weekly, EXCEPT Cinnamon Sugar (permanent)
- GF Mochi Muffins: flavors rotate daily among Black Sesame/Chocolate/Ube/Pandan
- Brioche Donuts: weekend-only, flavors rotate
- Drinks: a fixed list of 16 permanent drinks (mapped below); everything
  else in the drink categories is seasonal/limited-time

We classify every item into one of:
  - "Permanent Drink"      -> fair to compare individual item YoY
  - "Permanent Donut"      -> Cinnamon Sugar mochi donut, fair to compare YoY
  - "Rotating: Mochi Donut Flavor"
  - "Rotating: GF Muffin Flavor"
  - "Rotating: Brioche Donut Flavor"
  - "Other / Seasonal"     -> everything else (specials, merch, misc, etc.)

Input:  cleaned_sales.csv
Output: classified_sales.csv
"""
import pandas as pd

df = pd.read_csv("cleaned_sales.csv")

# Owner-given name -> actual Square item name (confirmed by checking each
# has meaningful sales in both years)
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
# Note: "Brown Sugar Oat Latte" doesn't appear in the data (negligible/new), excluded.

PERMANENT_DONUT_FLAVORS = {"MD: Cinnamon Sugar"}

ROTATING_CATEGORY_MAP = {
    "Mochi Donuts": "Rotating: Mochi Donut Flavor",
    "Gf Mochi Muffins": "Rotating: GF Muffin Flavor",
    "Brioche Donuts": "Rotating: Brioche Donut Flavor",
}


def classify(row):
    name = row["Item Name"]
    if name in PERMANENT_DRINKS:
        return "Permanent Drink"
    if name in PERMANENT_DONUT_FLAVORS:
        return "Permanent Donut"
    if row["Category"] in ROTATING_CATEGORY_MAP:
        return ROTATING_CATEGORY_MAP[row["Category"]]
    return "Other / Seasonal"


df["menu_type"] = df.apply(classify, axis=1)

reverse_map = {sq: own for own, sq in PERMANENT_DRINKS.items()}
df["display_name"] = df["Item Name"].map(reverse_map).fillna(df["Item Name"])

print("Revenue by menu_type:")
print(df.groupby("menu_type")["Net Sales"].sum().sort_values(ascending=False).round(0))

df.to_csv("classified_sales.csv", index=False)
print("\nSaved -> classified_sales.csv")
