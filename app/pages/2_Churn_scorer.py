"""Page 2: churn scorer (Part E model)."""
import math
from pathlib import Path

import joblib
import pandas as pd
import streamlit as st

MODEL_FILE = Path(__file__).resolve().parents[1] / "models" / "churn_model.joblib"
NUM = ["recency_days", "frequency", "total_spend", "avg_spend", "discount_share", "tenure_days",
       "pct_rain", "avg_delivery_min", "pct_cancelled", "age"]
CAT = ["city", "gender", "plan_type", "acquisition_channel"]
NOT_NEGATIVE = ["recency_days", "frequency", "total_spend", "avg_spend", "tenure_days"]
MAX_ROWS = 50_000


@st.cache_resource
def load_model():
    return joblib.load(MODEL_FILE) if MODEL_FILE.exists() else None


st.title("Churn scorer")
model = load_model()
if model is None:
    st.error("Model file app/models/churn_model.joblib not found. Save it from 03_churn.ipynb.")
    st.stop()

st.write("Upload a CSV in the customer feature-table format. Required columns: "
         + ", ".join(NUM + CAT) + ". Other columns (such as customer_id) are kept in the output.")
upload = st.file_uploader("Customer feature table (CSV)", type="csv")
if upload is None:
    st.stop()

try:
    df = pd.read_csv(upload)
except Exception:
    st.error("This file could not be read as a CSV.")
    st.stop()

missing = [c for c in NUM + CAT if c not in df.columns]
if df.empty:
    st.error("The file has no rows.")
elif len(df) > MAX_ROWS:
    st.error(f"The file has {len(df):,} rows. The limit is {MAX_ROWS:,}.")
elif missing:
    st.error("Missing required columns: " + ", ".join(missing))
else:
    numeric = {c: pd.to_numeric(df[c], errors="coerce") for c in NUM}
    not_numbers = [c for c in NUM if numeric[c].isna().sum() > df[c].isna().sum()]
    negatives = [c for c in NOT_NEGATIVE if (numeric[c] < 0).any()]
    if not_numbers:
        st.error("These columns contain non-numeric values: " + ", ".join(not_numbers))
    elif negatives:
        st.error("These columns contain negative values, which is not valid: " + ", ".join(negatives))
    else:
        df = df.assign(**numeric)
        probability = model.predict_proba(df[NUM + CAT])[:, 1]
        scored = df.assign(churn_probability=probability.round(4)).sort_values("churn_probability", ascending=False)
        scored.insert(0, "risk_rank", range(1, len(scored) + 1))
        top = scored.head(max(1, math.ceil(0.10 * len(scored))))

        left, middle, right = st.columns(3)
        left.metric("Customers scored", f"{len(scored):,}")
        middle.metric("Top 10% list", f"{len(top):,} customers")
        right.metric("Lowest probability in top 10%", f"{top.churn_probability.min():.2f}")
        st.subheader("Top 10% riskiest customers")
        st.dataframe(top, width="stretch")
        st.download_button("Download top 10% (CSV)", top.to_csv(index=False).encode("utf-8"),
                           "top10_churn_risk.csv", "text/csv")
        st.download_button("Download all scores (CSV)", scored.to_csv(index=False).encode("utf-8"),
                           "all_churn_scores.csv", "text/csv")
        st.caption("Use the ranking. The model is class-weighted, so the probabilities are higher than "
                   "the real churn rate (about 9%).")
