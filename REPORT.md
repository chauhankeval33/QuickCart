# QuickCart Assessment — Report

Max 4 pages. Lead each section with the answer, then the evidence.

## Part A — SQL
Result tables for A1–A6.

**Written question:** Which queries would be slow on 100M rows, and which index would you add?

## Part B — MongoDB
Results for B1–B5, including explain() before/after.

**Written question:** MongoDB vs PostgreSQL for this data?

## Part C — EDA and feature engineering
### 3. Delivery Drivers

1. **Distance:** Average delivery time increased from **20.24 minutes** for orders within 0–2 km to **36.27 minutes** for orders above 5 km — a difference of **16.03 minutes**.
2. **Store workload:** Average delivery time increased from **20.69 minutes** with 1–10 open orders to **27.56 minutes** with 21–29 open orders — a difference of **6.87 minutes**.
3. **Rain:** Rainy orders averaged **30.30 minutes**, compared with **23.69 minutes** during non-rainy conditions — an increase of **6.61 minutes**.

**Conclusion:** Distance showed the largest difference in average delivery time, followed by store workload and rain. These results show associations, not proof of causation.

### Data quality report
| Issue | Table.column | Count | How handled |
| --- | --- | --- | --- |
| | | | |

### Five findings
1.
2.
3.
4.
5.

**Written question:** Which features could leak information from after the cutoff date, and how did you prevent it?

## Part D — Delivery-time regression
| Model | MAE (min) | RMSE (min) |
| --- | --- | --- |
| Mean baseline | | |
| Linear | | |
| Ridge (alpha=) | | |
| Lasso (alpha=) | | |
| Tree model | | |

**Written question:** What delivery promise would you show in the app?

## Part E — Churn classification
Leakage findings:

| Model | ROC-AUC | PR-AUC | Precision | Recall |
| --- | --- | --- | --- | --- |
| Logistic Regression | | | | |
| Random Forest | | | | |
| XGBoost | | | | |
| LightGBM | | | | |

Profit-maximising threshold:
Top three churn drivers (plain English):

**Written question:** What would you monitor after deployment?

## Part F — Neural network
Comparison with best Part E model, and short answers.

## Part G — LLM ticket triage
| Approach | Accuracy on 60 labels |
| --- | --- |
| TF-IDF + LR | |
| Prompt v1 | |
| Prompt v2 | |

**Written question:** Two failure modes accuracy would not reveal.

## Part H — Power BI DAX measure
```
<paste your DAX here>
```

## Assumptions I made
-
