# Zomato Bangalore Restaurant Analytics

Exploratory Data Analysis of Bangalore's restaurant ecosystem using the Zomato Kaggle dataset. This project investigates pricing patterns, customer engagement, cuisine preferences, restaurant performance, and identifies underserved market opportunities across Bangalore.

---

## Project Overview

The objective of this project is to understand what drives restaurant success on Zomato and identify potential market gaps across Bangalore's restaurant landscape.

Using over 50,000 restaurant records, the analysis explores:

* Rating behaviour and customer preferences
* Restaurant pricing patterns
* Cuisine performance across locations
* Customer engagement trends
* Supply-demand imbalances
* Business expansion opportunities

---

## Dataset Information

| Property      | Value                                  |
| ------------- | -------------------------------------- |
| Source        | Zomato Bangalore Dataset (Kaggle)      |
| Raw Records   | 51,717                                 |
| Clean Records | 49,011                                 |
| Features Used | 15                                     |
| Coverage      | Bangalore restaurants listed on Zomato |

---

## Repository Structure

```text
zomato-analytics/
├── zomato.ipynb
├── zomato_analytics.ipynb
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

* Python
* Pandas
* NumPy
* Data Cleaning
* Exploratory Data Analysis
* Statistical Analysis
* Data Visualization
* Business Analytics
* Market Opportunity Analysis
* Customer Behaviour Analysis
* Insight Generation

---

## Data Cleaning & Preparation

Several data quality issues were identified and resolved before analysis.

### Data Quality Fixes

* Removed 2,474 corrupted rows where review text shifted into URL fields because of CSV formatting issues.
* Converted ratings from string format (`4.1/5`) into numerical values.
* Cleaned `approx_cost` by removing commas from values such as `1,200`.
* Replaced empty review lists (`[]`) with proper missing values.
* Removed highly incomplete columns:

  * `dish_liked` (54% missing)
  * `menu_item` (75% missing)
* Removed rows containing missing values in:

  * location
  * restaurant type
  * cuisines

---

## Visual Analysis

### Rating Distribution

Most restaurants are concentrated between ratings of 3.5 and 4.0, with an overall average rating of approximately 3.71.

![Rating Distribution](images/rating_distribution.png)

---

### Cost Distribution

The Bangalore restaurant market is heavily concentrated in the affordable segment, with a median cost-for-two of approximately ₹400.

![Cost Distribution](images/cost_distribution.png)

---

### Top Rated Cuisines Across High-Performing Locations

Premium neighbourhoods consistently favour niche and international cuisines over mainstream categories.

![Top Rated Cuisines](images/top_rated_cuisines.png)

---

### Highest-Voted Price Range by Location

Premium and luxury restaurants dominate customer engagement across Bangalore's highest-performing restaurant districts.

![Highest Voted Price Range](images/highest_voted_price_range.png)

---

## Analysis Framework

The project addresses 23 business questions across three analytical layers.

### Univariate Analysis

* Rating distribution
* Cost distribution
* Restaurant type distribution
* Category distribution

### Bivariate Analysis

* Online ordering vs ratings
* Table booking vs ratings
* Cost vs customer engagement
* Location performance
* Restaurant type performance

### Multivariate Analysis

* Cuisine quality by location
* Cuisine identity by restaurant type
* Category distribution by neighbourhood
* Price-range performance by area
* Supply-demand gap analysis

---

## Key Findings

### 1. Specialisation Beats Volume

Niche international cuisines consistently outperform mainstream categories.

Top-rated cuisines include:

* Japanese
* Korean
* Mediterranean
* Parsi
* Singaporean
* Indonesian

These cuisines achieve higher ratings than dominant categories such as North Indian, Chinese, and South Indian.

---

### 2. Dine-In Generates Significantly More Engagement

Customer engagement is strongly linked to sit-down dining experiences.

Example:

* Casual Dining (North Indian): ~2.6 million votes
* Delivery (North Indian): ~126 thousand votes

Customers are substantially more likely to review dine-in experiences than delivery orders.

---

### 3. Restaurant Types Have Distinct Cuisine Identities

Different restaurant formats serve different culinary markets.

**Cafes**

* Italian
* American
* Continental
* Burgers

**Casual Dining**

* North Indian
* Mughlai
* Biryani

Cuisine preference is strongly influenced by restaurant format.

---

### 4. Premium Spending Correlates with Higher Engagement

Higher-priced restaurants consistently attract greater customer interaction.

For example:

* Luxury restaurants on St. Marks Road average more than 5,000 votes.

The assumption that budget restaurants generate the highest engagement is not supported by the data.

---

### 5. East Bangalore Functions as a Dessert Hub

After excluding Delivery and Dine-Out categories, East Bangalore locations such as:

* Whitefield
* Bellandur
* Marathahalli

show Desserts as the dominant category.

This aligns with the area's young technology-focused demographic.

---

### 6. Four Areas Are Critically Underserved

| Location             | Restaurants | Avg Votes | Demand/Supply Ratio |
| -------------------- | ----------- | --------- | ------------------- |
| Rajarajeshwari Nagar | 2           | 366       | 183                 |
| Central Bangalore    | 3           | 383       | 128                 |
| West Bangalore       | 5           | 222       | 44                  |
| North Bangalore      | 7           | 229       | 33                  |

Three cuisine categories are absent from all four underserved zones:

* South Indian
* Cafe
* Desserts

These represent the strongest market-entry opportunities identified in the analysis.

---

## Business Recommendations

### Expansion Opportunities

* Expand South Indian offerings in underserved zones.
* Introduce cafe concepts in low-supply regions.
* Develop dessert-focused outlets in emerging residential areas.

### Customer Engagement Strategy

* Invest in dine-in experiences for high-engagement cuisine categories.
* Increase visibility for highly rated niche cuisines.
* Focus premium dining concepts on high-demand neighbourhoods.

### Market Positioning

* Premium dining demonstrates the strongest customer engagement.
* Niche cuisine concepts achieve higher customer satisfaction.
* Underserved locations provide lower competition and higher growth potential.

---

## Future Enhancements

Potential extensions of this project include:

* Interactive Power BI dashboard
* Restaurant rating prediction model
* Customer sentiment analysis
* Restaurant recommendation engine
* Restaurant success classification model

---

## Installation

```bash
git clone https://github.com/yashvardhandebas/zomato-analytics.git

cd zomato-analytics

pip install pandas numpy matplotlib seaborn jupyter
```

Download the Zomato Bangalore dataset from Kaggle and place:

```text
zomato.csv
```

in the project root directory.

Run:

```bash
jupyter notebook zomato_analytics.ipynb
```

---

## Dependencies

* pandas >= 1.5
* numpy >= 1.23
* matplotlib >= 3.6
* seaborn >= 0.12
* jupyter

---

## Author

Yashvardhan Debas

GitHub: https://github.com/yashvardhandebas
