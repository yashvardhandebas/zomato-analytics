# Zomato Bangalore — Restaurant Analytics

Exploratory data analysis of Bangalore's restaurant ecosystem using the Zomato Kaggle dataset. The project investigates pricing patterns, rating drivers, cuisine preferences, location performance, and identifies underserved market zones across the city.

---

## Dataset

| Property | Value |
|---|---|
| Source | [Zomato Bangalore Dataset — Kaggle](https://www.kaggle.com/datasets/himanshupoddar/zomato-bangalore-restaurants) |
| Raw rows | 51,717 |
| Clean rows | 49,011 |
| Columns used | 15 |
| Coverage | Bangalore restaurants listed on Zomato |

---

## Project Structure

```
zomato-analytics/
├── zomato.csv                  # raw dataset (not tracked by git)
├── zomato_analytics.ipynb      # full analysis notebook
├── README.md
└── .gitignore
```

---

## What's Covered

### Data Cleaning
- Removed 2,474 rows with corrupted URLs (review text shifted into URL column due to unescaped commas in the CSV)
- Converted `rate` from string `'4.1/5'` to float `4.1`
- Cleaned `approx_cost` — stripped commas from values like `'1,200'`
- Replaced empty `[]` in `reviews_list` with proper `NaN`
- Dropped `dish_liked` (54% missing) and `menu_item` (75% missing)
- Dropped 232 rows with nulls in `location`, `rest_type`, `cuisines`

### Analysis (23 questions across 3 layers)

**Univariate** — distribution of ratings, costs, restaurant types, categories

**Bivariate** — online ordering vs rating, table booking vs rating, price range vs votes, location vs count/rating/cost, rest type vs rating/votes

**Multivariate** — cuisine quality by location, cuisine identity per restaurant type, category distribution by neighbourhood, price range performance by area, supply-demand gap analysis

---

## Key Findings

**1. Specialisation beats volume**
Niche international cuisines — Japanese, Korean, Mediterranean, Parsi — consistently outrate the most common cuisines (North Indian, Chinese, South Indian) across every premium location. Lavelle Road's top-rated cuisine: Juices at 4.60. St. Marks Road's top cluster: Southeast Asian at 4.54.

**2. Dine-in drives 20× more engagement than delivery**
Casual Dining generates 2.6M total votes for North Indian alone. The same cuisine via Delivery generates 126k. People vote significantly more when they've had a sit-down experience.

**3. Restaurant types have distinct cuisine identities**
Cafes are overwhelmingly Western (Burger, Continental, Italian, American). Casual Dining is Indian (North Indian, Mughlai, Biryani). These aren't overlapping — they're separate food cultures operating under the same platform.

**4. Higher spend = higher engagement**
Budget restaurants are absent from every top-voted location. Luxury (₹2,000+) averages 5,277 votes in St. Marks Road. The assumption that affordable restaurants are more popular is not supported by this data.

**5. East Bangalore is a dessert zone**
When Delivery and Dine-out are excluded, East Bangalore (IT corridor — Whitefield, Marathahalli, Bellandur) uniquely shows Desserts as its dominant category. Consistent with the young tech-worker demographic and snacking culture in that area.

**6. Four areas are critically underserved**

| Location | Restaurants | Avg Votes | Demand/Supply Ratio |
|---|---|---|---|
| Rajarajeshwari Nagar | 2 | 366 | **183** |
| Central Bangalore | 3 | 383 | **128** |
| West Bangalore | 5 | 222 | 44 |
| North Bangalore | 7 | 229 | 33 |

Three cuisine categories are missing from **all four** underserved areas: South Indian, Cafe, and Desserts. These represent the clearest entry points for new restaurant operators.

---

## Setup

```bash
git clone https://github.com/yashvardhandebas/zomato-analytics.git
cd zomato-analytics
pip install pandas numpy matplotlib seaborn jupyter
```

Download `zomato.csv` from [Kaggle](https://www.kaggle.com/datasets/himanshupoddar/zomato-bangalore-restaurants) and place it in the project root.

```bash
jupyter notebook zomato_analytics.ipynb
```

---

## Dependencies

```
pandas >= 1.5
numpy >= 1.23
matplotlib >= 3.6
seaborn >= 0.12
jupyter
```

---

## Author

**Yashvardhan Debas**
[github.com/yashvardhandebas](https://github.com/yashvardhandebas)
