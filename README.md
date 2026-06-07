# Zomato Bangalore — Restaurant Analytics

Exploratory data analysis and restaurant success prediction using the Zomato Bangalore Kaggle dataset. The project investigates what drives restaurant popularity on Zomato — and builds a machine learning model to predict it.

> **49,011 restaurants · 23 EDA questions · 3 statistical tests · 3 ML models · ROC-AUC 0.89**

---

## Project Overview

Most Zomato EDA projects stop at bar charts. This one goes further — every major claim is statistically validated, a binary classification model predicts restaurant success with 80% accuracy, and findings are framed as business recommendations rather than observations.

The analysis covers:
- What drives ratings — and what doesn't (online ordering turns out not to matter for satisfaction)
- Cuisine performance across Bangalore's neighbourhoods
- Which price ranges actually generate customer engagement
- Where demand far exceeds supply — the real market opportunity
- Predicting whether a restaurant will achieve above-median engagement before it accumulates a vote history

---

## Dataset

| Property | Value |
|---|---|
| Source | [Zomato Bangalore Dataset — Kaggle](https://www.kaggle.com/datasets/himanshupoddar/zomato-bangalore-restaurants) |
| Raw records | 51,717 |
| Clean records | 49,011 |
| Features used | 15 |
| Coverage | Bangalore restaurants listed on Zomato |

---

## Repository Structure

```text
zomato-analytics/
├── zomato_analytics_final.ipynb  # full analysis + ML model
├── images/
│   ├── rating_distribution.png
│   ├── cost_distribution.png
│   ├── top_rated_cuisines.png
│   └── highest_voted_price_range.png
├── README.md
└── .gitignore
```

---

## Skills Demonstrated

`Python` `Pandas` `NumPy` `Seaborn` `Matplotlib` `Scikit-learn` `XGBoost` `Statistical Testing` `Binary Classification` `Feature Engineering` `EDA` `Data Cleaning` `Business Analytics` `Market Analysis`

---

## Data Cleaning

| Issue | Fix |
|---|---|
| 2,474 rows with review text in URL column | Dropped — CSV comma-escaping failure, unrecoverable |
| `rate` stored as `'4.1/5'` string | Stripped `/5`, converted to float |
| `approx_cost` with commas (`'1,200'`) | Stripped commas, converted to float |
| `reviews_list` empty brackets (`[]`) | Replaced with `NaN` |
| `dish_liked` — 54% missing | Column dropped |
| `menu_item` — 75% missing | Column dropped |
| Sparse nulls in location, rest_type, cuisines | 232 rows dropped |

---

## Visual Analysis

### Rating Distribution

Most restaurants cluster between 3.5 and 4.0. Mean rating: 3.71. The distribution is left-skewed — very few restaurants fall below 3.0 or above 4.5.

![Rating Distribution](images/rating_distribution.png)

---

### Cost Distribution

Bangalore's restaurant market is concentrated in the affordable segment. Median cost-for-two: approximately ₹400. A long right tail of luxury restaurants pulls the mean higher.

![Cost Distribution](images/cost_distribution.png)

---

### Top Rated Cuisines Across High-Performing Locations

Premium neighbourhoods consistently favour niche international cuisines — Japanese, Korean, and Mediterranean outrate North Indian and Chinese everywhere.

![Top Rated Cuisines](images/top_rated_cuisines.png)

---

### Highest-Voted Price Range by Location

Premium and luxury restaurants dominate customer engagement. Budget restaurants do not appear in any location's top-voted category.

![Highest Voted Price Range](images/highest_voted_price_range.png)

---

## Analysis Framework

23 questions answered across three layers — univariate first, then bivariate, then multivariate.

### Layer 1 — Univariate
Rating distribution · Cost distribution · Restaurant type breakdown · Category breakdown

### Layer 2 — Bivariate
Online ordering vs rating · Table booking vs rating · Cost vs engagement · Location performance · Restaurant type performance

### Layer 3 — Multivariate
Cuisine quality by location · Cuisine identity per restaurant type · Category distribution by neighbourhood · Price-range performance by area · Supply-demand gap analysis

---

## Statistical Validation

Three core claims tested formally — not just reported from groupby means.

### Test 1 — Online Ordering vs Rating (Mann-Whitney U)
```
Online Yes:  mean 3.726  (n = 29,013)
Online No:   mean 3.677  (n = 19,998)
p-value:     < 0.0001
Difference:  0.049 rating points
```
**Verdict:** Statistically significant but practically negligible. A 0.049 point gap on a 5-point scale is imperceptible to customers. Online ordering availability does not meaningfully drive ratings.

---

### Test 2 — Table Booking vs Rating (Mann-Whitney U)
```
Book Yes:   mean 4.136  (n = 6,345 — 13% of restaurants)
Book No:    mean 3.642  (n = 42,666)
p-value:    < 0.0001
Difference: 0.494 rating points
```
**Verdict:** Statistically significant and practically meaningful. Nearly half a rating point difference. Table booking is a proxy for restaurant quality tier — restaurants offering reservations self-select into a higher operating standard. Correlation, not causation.

---

### Test 3 — Cost vs Rating (Spearman Correlation)
```
Spearman r:         0.358
p-value:            < 0.0001
Variance explained: ~13%
```
**Verdict:** Moderate-strong positive correlation. Higher cost associates with better ratings but explains only 13% of rating variance. Service, cuisine quality, and management drive the remaining 87%.

---

## Machine Learning — Restaurant Success Prediction

**Business question:** Can we predict whether a restaurant will achieve above-median customer engagement given only its structural features — before it accumulates a vote history?

### Target Variable
```
success = 1  if votes > median votes  (popular)
success = 0  if votes ≤ median votes  (not popular)
Class balance: 50.06% / 49.93% — perfectly balanced
```

### Feature Engineering
- `online_order`, `book_table` → binary encoded (Yes=1, No=0)
- `approx_cost` → used as-is (float)
- `location` → target encoded as mean success rate per area (avoids one-hot explosion across 80+ locations)
- `cuisines` → top 10 cuisines extracted as binary flag columns
- `rest_type`, `listed_in(type)` → one-hot encoded

### Model Results

| Model | Accuracy | F1 | ROC-AUC | CV F1 (5-fold) |
|---|---|---|---|---|
| Logistic Regression | 75.35% | 0.7531 | 0.8420 | 0.7400 ± 0.004 |
| Random Forest | 76.07% | 0.7593 | 0.8536 | 0.7391 ± 0.004 |
| **XGBoost** | **80.22%** | **0.8021** | **0.8903** | **0.7937 ± 0.003** |

**XGBoost selected as production model.** ROC-AUC of 0.89 means the model correctly ranks a popular restaurant above an unpopular one 89% of the time. Low CV standard deviation confirms stability — the model is not overfitting to one test split.

### Why XGBoost Wins on the Metric That Matters

False negatives — popular restaurants the model fails to identify — are the costly error for this business use case. XGBoost misses 1,102 popular restaurants vs Random Forest's 1,537. That's 435 fewer missed opportunities, which is why XGBoost wins beyond headline accuracy.

### Top 5 Feature Importances (Random Forest)

| Feature | Importance | Interpretation |
|---|---|---|
| approx_cost | 0.26 | Price tier is the single strongest signal of engagement |
| book_table | 0.16 | Reservation capability signals quality tier |
| online_order | 0.13 | Drives discoverability without improving satisfaction |
| location | 0.11 | Neighbourhood success rate matters significantly |
| rest_type_Casual Dining | 0.09 | Format identity is a real predictor, not noise |

### The online_order Contradiction — Resolved

The Mann-Whitney test shows online ordering has negligible effect on **ratings** (Δ = 0.049). The model shows it has substantial importance for predicting **votes** (importance = 0.13). These are not contradictory — they measure different things. Online ordering gets restaurants discovered and voted on. It does not make the food or experience better. Two separate mechanisms, both confirmed by data.

---

## Key EDA Findings

### 1. Specialisation beats volume
Niche international cuisines — Japanese, Korean, Mediterranean, Parsi — consistently outrate the most common cuisines regardless of location. The cuisines ordered most are not the ones rated highest.

### 2. Dine-in generates 20× more engagement than delivery
Casual Dining (North Indian): ~2.6M total votes. Delivery (North Indian): ~126k votes. Customers are far more likely to engage and review sit-down experiences than delivery orders.

### 3. Restaurant types have distinct cuisine identities

| Format | Top Cuisines |
|---|---|
| Cafes | Burger · Continental · Italian · American |
| Casual Dining | North Indian · Mughlai · Biryani |
| Quick Bites | North Indian · Fast Food · Chinese |
| Delivery | North Indian · Biryani · Chinese |

### 4. Premium spending drives engagement — budget does not
Luxury restaurants (₹2,000+) on St. Marks Road average 5,277 votes. Budget restaurants do not appear in any location's top-voted category.

### 5. East Bangalore is a dessert zone
Excluding Delivery and Dine-Out, East Bangalore (Whitefield, Bellandur, Marathahalli) is the only zone where Desserts dominates. Consistent with the IT corridor's young tech-worker demographic.

### 6. Four areas are critically underserved

| Location | Restaurants | Avg Votes | Demand/Supply Ratio |
|---|---|---|---|
| Rajarajeshwari Nagar | 2 | 366 | **183** |
| Central Bangalore | 3 | 383 | **128** |
| West Bangalore | 5 | 222 | 44 |
| North Bangalore | 7 | 229 | 33 |

Three cuisine categories absent from all four underserved zones: **South Indian · Cafe · Desserts**

---

## Business Recommendations

**For restaurant operators:**
- Rajarajeshwari Nagar has a demand/supply ratio of 183 with only 2 restaurants. A South Indian or Cafe concept here faces near-zero competition with demonstrated existing demand.
- Price positioning in the Premium (₹1k-2k) bracket maximises engagement. The model confirms approx_cost as the strongest predictor (importance = 0.26).
- Enabling both online ordering and table booking together maximises discoverability — the model ranks both in the top 3 features.

**For Zomato:**
- Online ordering campaigns will not improve customer satisfaction scores — the Mann-Whitney test confirms the practical difference is negligible (Δ = 0.049).
- Table booking restaurants (13% of listings) generate disproportionately high ratings and engagement — quality-tier acquisition outperforms volume-based acquisition.
- The four underserved zones represent genuine growth opportunities where restaurant recruitment meets existing unmet demand.

**Model limitation:**
Votes are partly a function of listing age — a restaurant listed in 2015 accumulates votes passively over time. This analysis does not control for listing age. A normalised votes-per-month metric would improve target variable quality in future iterations.

---

## Future Enhancements

- [x] EDA — 23 business questions answered
- [x] Statistical validation — 3 claims tested with Mann-Whitney U and Spearman
- [x] ML model — XGBoost binary classifier, ROC-AUC 0.89
- [ ] Interactive Power BI dashboard with location drill-down
- [ ] Votes normalisation by listing age for improved demand proxy
- [ ] Customer sentiment analysis on reviews_list
- [ ] Restaurant recommendation engine

---

## Setup

```bash
git clone https://github.com/yashvardhandebas/zomato-analytics.git
cd zomato-analytics
pip install pandas numpy matplotlib seaborn scipy scikit-learn xgboost jupyter
```

Download `zomato.csv` from [Kaggle](https://www.kaggle.com/datasets/himanshupoddar/zomato-bangalore-restaurants) and place in the project root, then:

```bash
jupyter notebook zomato_analytics_final.ipynb
```

---

## Dependencies

```
pandas >= 1.5
numpy >= 1.23
matplotlib >= 3.6
seaborn >= 0.12
scipy >= 1.9
scikit-learn >= 1.1
xgboost >= 1.7
jupyter
```

---

## Author

**Yashvardhan Debas**
[github.com/yashvardhandebas](https://github.com/yashvardhandebas)
