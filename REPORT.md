# QuickCart Assessment Report

**Candidate:** Keval Chauhan  
**Project:** QuickCart Data Analytics and AI Assessment

## Part A — SQL Analysis

SQL is used to extract, filter, aggregate, and analyze order and customer data. The queries in this project are intended to identify business trends, customer behavior, order performance, and operational bottlenecks.

**Approach and next steps:**
- Use joins to combine relevant order, customer, store, and delivery tables.
- Apply `WHERE`, `GROUP BY`, aggregate functions, and `HAVING` to answer business questions.
- Use CTEs and window functions where ranking, running totals, or comparisons between records are required.
- Validate the results against the underlying data and document the business interpretation of each query.

**Status:** Final query outputs and validated numerical findings should be added after running and checking all SQL tasks.

## Part B — MongoDB Analysis

MongoDB is suitable for analyzing semi-structured order and customer documents. Aggregation pipelines can filter records, group them, calculate summary statistics, and sort the results.

**Approach and next steps:**
- Use `$match` to filter relevant documents.
- Use `$group` with operators such as `$sum` and `$avg` to calculate business metrics.
- Use `$project` to select and transform fields and `$sort` to rank results.
- Validate aggregation results against equivalent SQL results where the underlying data and definitions match.

**Status:** Run and verify each MongoDB query, then add the relevant outputs and business conclusions.

## Part C — Exploratory Data Analysis (EDA)

The analysis examined relationships between delivery time and selected operational factors.

| Factor | Group 1 | Group 2 | Difference |
|---|---:|---:|---:|
| Delivery distance | 0–2 km: 20.24 min | Above 5 km: 36.27 min | 16.03 min |
| Open-order workload | 1–10 orders: 20.69 min | 21–29 orders: 27.56 min | 6.87 min |
| Weather | Non-rainy: 23.69 min | Rainy: 30.30 min | 6.61 min |

**Key findings:**
1. Orders traveling more than 5 km had a higher average delivery time than orders traveling 0–2 km.
2. Higher open-order workload was associated with longer average delivery times.
3. Average delivery time was higher during rainy conditions than during non-rainy conditions.

These results show associations, not proof of causation. Other factors, including traffic, store preparation time, location, and staffing, may also affect delivery performance.

**Next steps:** Analyze these relationships by store, time period, and order volume. Check sample sizes and distributions, investigate outliers, and use appropriate statistical tests before drawing stronger conclusions.

## Part D — Regression Analysis

Regression can help estimate a continuous business outcome, such as delivery time, using relevant order and operational features.

**Approach and next steps:**
- Define the target variable and identify features available at prediction time.
- Split the data into training and test sets, avoiding leakage between them.
- Establish a baseline model and compare it with suitable regression algorithms.
- Evaluate performance using MAE and RMSE; use additional metrics if appropriate for the business objective.
- Inspect residuals and errors to identify groups where predictions are less accurate.

**Status:** Add the selected model, test-set metrics, and interpretation after completing and validating the regression experiments.

## Part E — Customer Churn Classification

Churn classification estimates whether a customer is likely to stop using a service. Model evaluation should consider the business cost of missed churners as well as overall accuracy.

**Approach and next steps:**
- Inspect the target distribution and preprocess numeric and categorical features.
- Establish a baseline and compare suitable classification models.
- Evaluate precision, recall, F1-score, confusion matrix, and ROC-AUC where appropriate.
- Select the classification threshold based on the business objective rather than accuracy alone.
- Check for data leakage and evaluate the final model on unseen data.

**Status:** Add the validated test-set results, selected threshold, and business recommendations after running the final experiments.

## Part F — Neural Network

A neural network can learn nonlinear patterns from appropriately prepared data. Its usefulness should be assessed against simpler baseline models.

**Approach and next steps:**
- Prepare the features and target, applying suitable encoding and scaling.
- Train a baseline neural network with a suitable output layer and loss function.
- Monitor validation performance and use early stopping or regularization to reduce overfitting.
- Compare test-set performance with the relevant baseline model.

**Status:** Report the final architecture, training configuration, and evaluation metrics once the experiment is complete.

## Part G — LLM-Based Support Ticket Triage

The LLM workflow classifies support tickets into business categories. The evaluation compared two prompt versions and a traditional machine-learning baseline.

**Results:**

| Method | Evaluation result | Failed calls |
|---|---:|---:|
| Prompt v1 | 59/60 correct (98.3%) | 0 |
| Prompt v2 | 60/60 correct (100%) | 0 |
| TF-IDF + Logistic Regression | 78.3% five-fold cross-validation accuracy | Not applicable |

The evaluation script processed 42 unique tickets per prompt, despite reporting 60 evaluation rows. This discrepancy should be investigated before treating the results as a fully verified comparison. The cross-validation result is also not directly comparable to the separate 60-row prompt evaluation.

**Batch execution results:**
- Tickets processed: 400
- Failed tickets: 0
- API calls: 222
- Total runtime: approximately 14.5 minutes
- Retries for invalid output: 0
- API errors or rate limits: 0
- Tokens: 187,545 input and 44,226 output
- Reported cost: $0 on the free tier

**Category distribution:**

| Category | Tickets |
|---|---:|
| late_delivery | 111 |
| missing_item | 84 |
| payment_refund | 54 |
| quality | 53 |
| app_bug | 50 |
| praise | 48 |
| **Total** | **400** |

