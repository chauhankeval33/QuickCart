# QuickCart Data Science Assessment Report

**Candidate:** Keval Chauhan | **Repository:** [QuickCart](https://github.com/chauhankeval33/QuickCart)

## Part A — SQL (12 points)

**Written answer — Performance and indexing:** Queries involving full-table scans, `DISTINCT`, large aggregations, window functions, and customer-level cohort calculations may become expensive at 100 million rows. I would inspect query plans using `EXPLAIN QUERY PLAN`, add indexes on frequently filtered or joined columns such as `orders(customer_id)`, `orders(order_ts)`, and `orders(status)`, and validate whether composite indexes improve the actual queries. Indexes should be chosen based on query patterns because they increase storage and write costs.

**Remaining work:** Execute all six SQLite queries, include their result tables, and document data-audit counts, city cleanup, monthly GMV growth, top customers, cohort retention, and delivery time by hour.

## Part B — MongoDB (8 points)

**Written answer — MongoDB versus PostgreSQL:** MongoDB is useful for nested, semi-structured documents such as app sessions containing device information and arrays of events. It supports flexible document structures and aggregation pipelines. PostgreSQL is generally preferable for highly relational data, transactions, strict schemas, and queries requiring complex joins and strong relational constraints. The choice depends on access patterns, consistency requirements, and operational needs.

**Index:** For customer session lookups over a date range, I would test a compound index on `{customer_id: 1, session_start: -1}` and compare query execution statistics before and after using `explain("executionStats")`.

**Remaining work:** Run all five aggregation tasks, report funnel conversion rates and app-version comparisons, and capture actual before/after query plans.

## Part C — EDA and Feature Engineering (14 points)

### Delivery-time findings

| Factor | Group 1 | Group 2 | Difference |
|---|---:|---:|---:|
| Distance | 0–2 km: 20.24 min | Above 5 km: 36.27 min | 16.03 min |
| Open orders | 1–10: 20.69 min | 21–29: 27.56 min | 6.87 min |
| Weather | Non-rainy: 23.69 min | Rainy: 30.30 min | 6.61 min |

Longer distances, greater store workload, and rainy conditions were associated with longer average delivery times. These are observational comparisons, not proof of causation. Sample sizes, outliers, city differences, and other confounders should be checked.

**Feature leakage — written answer:** Recency, frequency, spend, discount share, cancellation rate, rain exposure, and average delivery time can leak future information if calculated using orders after the prediction cutoff. I would filter orders to timestamps on or before 30 June 2026 before calculating customer features, and calculate tenure relative to that cutoff. The churn label uses behavior in the following 60 days and must remain the target, not an input feature. I would verify leakage by comparing candidate features with their source records and confirming that no post-cutoff records contribute.

**Remaining work:** Document all data-quality issues, their counts and treatments; include exactly five charts with one business finding each; and compare vectorized recency computation with a loop using `%timeit`.

## Part D — Delivery-Time Regression (12 points)

**Written answer — Promised delivery time:** I would not promise the predicted mean as a guaranteed delivery time because individual delivery times vary and some orders take longer than average. I would estimate a calibrated upper prediction quantile or prediction interval and choose a service level, such as the 90th percentile, based on the business trade-off between reliability and customer expectations. Calibration should be checked on held-out data.

**Remaining work:** Report mean-baseline and linear-regression MAE/RMSE; compare Ridge, Lasso, and a tree-based model; tune regularization with five-fold cross-validation; identify coefficients driven to zero by Lasso; quantify rain and distance effects; and analyze residuals. Use only features available when the order is placed.

## Part E — Churn Classification (18 points)

**Written answer — Monitoring a monthly model:** I would monitor feature and prediction drift, missing values, churn prevalence, probability calibration, and performance metrics such as ROC-AUC, PR-AUC, precision, and recall once actual churn labels become available. I would compare these metrics with a validated baseline and investigate changes by city and customer segment. Because labels arrive after the prediction period, I would account for label delay and avoid treating unlabelled predictions as confirmed errors. Retraining would follow predefined performance or drift thresholds, followed by validation before deployment.

**Remaining work:** Quantify leakage with evidence, report churn rate and the limitations of accuracy under class imbalance, compare all four required models on the same stratified split, tune the best model for at least 20 trials, maximize test-set retention profit using the ₹150 offer cost and ₹1,200 saved-customer value, and report feature importance and model metrics.

## Part F — Deep Learning (8 points)

**Backpropagation:** Backpropagation calculates how much each model parameter contributes to prediction error by propagating gradients from the output layer back through the network. An optimizer uses these gradients to update the parameters and reduce the loss.

**Activation function:** ReLU is a common hidden-layer activation because it introduces nonlinearity and is computationally efficient. A sigmoid output is suitable for binary churn classification when producing a probability.

**Overfitting:** If training loss decreases while validation loss rises, I would use early stopping, review dropout or weight decay, and check data leakage and the train/validation split. I would select the checkpoint with the best validation performance.

**Remaining work:** Report the neural network's ROC-AUC and PR-AUC beside the best Part E model, plot training and validation loss, and justify which model to deploy based on performance, reliability, and operational complexity.

## Part G — LLM Ticket Triage (12 points)

### Reported evaluation

| Method | Reported result |
|---|---:|
| Prompt v1 | 59/60 correct (98.3%) |
| Prompt v2 | 60/60 correct (100%) |
| TF-IDF + Logistic Regression | 78.3% five-fold cross-validation accuracy |

The evaluation script processed only 42 unique tickets per prompt despite reporting 60 evaluation rows. Therefore, these accuracy figures require verification before being treated as a definitive comparison. The cross-validation result is not directly comparable to the separate prompt evaluation.

**Batch run:** 400 tickets processed; 0 failed tickets; 222 API calls; approximately 867 seconds; 0 invalid-output retries; 0 API errors or rate limits; 187,545 input tokens and 44,226 output tokens. Reported cost was $0 on the free tier.

**Category counts:** late_delivery 111; missing_item 84; payment_refund 54; quality 53; app_bug 50; praise 48.

**Written answer — Two failure modes and safeguards:**

1. **Invalid or fabricated outputs:** An LLM may return malformed JSON, an unsupported category, or an urgency outside the allowed range. Use schema validation, retries with limits, and a safe fallback or manual-review queue.
2. **Ambiguous or mixed complaints:** Hinglish or tickets describing multiple issues may be assigned the wrong category or urgency. Define category precedence, test multilingual and multi-issue examples, and manually review uncertain cases.

Accuracy on 60 examples cannot establish reliability across all languages, rare cases, changing ticket patterns, or production conditions.

**Remaining work:** Resolve the unique-ticket discrepancy, verify both confusion matrices against the 60 labelled tickets, report category-level metrics, and evaluate on an independent labelled set.

## Part H — Streamlit and Power BI (10 points)

The Streamlit application is intended to provide three workflows: delivery-time estimation, customer churn scoring, and support-ticket triage. Inputs should be validated, models loaded with `st.cache_resource`, and secrets stored in Streamlit secrets rather than source code.

**Example DAX measure — Repeat-customer rate:**

```dax
Repeat Customer Rate =
DIVIDE(
    CALCULATE(
        DISTINCTCOUNT(Orders[customer_id]),
        FILTER(
            VALUES(Orders[customer_id]),
            CALCULATE(DISTINCTCOUNT(Orders[order_id])) > 1
        )
    ),
    DISTINCTCOUNT(Orders[customer_id]),
    0
)
```

This measure calculates the share of customers with more than one distinct order in the current filter context. The result depends on the selected date range and report filters.

**Remaining work:** Validate the delivery estimator and churn scorer against the trained models; test invalid inputs and downloads; verify the ticket-triage output; and complete the Power BI KPI cards, monthly GMV trend, city/hour delivery matrix, city slicer, and DAX measure. Submit both the `.pbix` file and PDF export.

## Part I — Git and Submission (6 points)

The public repository is [github.com/chauhankeval33/QuickCart](https://github.com/chauhankeval33/QuickCart). Changes have been pushed to the `main` branch.

