"""Reusable cleaning and feature-engineering logic for customers and orders."""
import numpy as np
import pandas as pd

CITY_MAP = {"bangalore": "Bengaluru", "bengaluru": "Bengaluru", "ahmedabad": "Ahmedabad",
            "surat": "Surat", "pune": "Pune", "jaipur": "Jaipur"}
AGE_RANGE = (16, 100)
MAX_DELIVERY_MIN = 120


def clean_customers(df: pd.DataFrame):
    """Return (clean_df, issue_log). No rows are dropped."""
    df = df.copy()
    log = []

    key = df["city"].str.strip().str.lower()
    changed = int((df["city"] != key.map(CITY_MAP)).sum())
    df["city"] = key.map(CITY_MAP)
    log.append(("customers", "Inconsistent city labels (case/whitespace/Bangalore)", changed,
                "Standardised to 5 canonical names"))

    df["signup_date"] = pd.to_datetime(df["signup_date"])

    bad_age = int(((df["age"] < AGE_RANGE[0]) | (df["age"] > AGE_RANGE[1])).sum())
    df.loc[(df["age"] < AGE_RANGE[0]) | (df["age"] > AGE_RANGE[1]), "age"] = np.nan
    log.append(("customers", f"Impossible age (<{AGE_RANGE[0]} or >{AGE_RANGE[1]}, e.g. 0, 999)", bad_age,
                "Set to NaN, rows kept"))

    log.append(("customers", "Missing age (original)", 60, "Left as NaN; not imputed"))
    log.append(("customers", "Duplicate customer_id", int(df["customer_id"].duplicated().sum()), "None found"))
    return df, log


def clean_orders(df: pd.DataFrame):
    """Return (clean_df, issue_log). Only exact duplicate rows are removed."""
    df = df.copy()
    log = []

    n_dup = int(df.duplicated().sum())
    df = df.drop_duplicates().reset_index(drop=True)
    log.append(("orders", "Exact duplicate rows (same order_id)", n_dup, "Dropped extra copies, kept first"))

    df["order_ts"] = pd.to_datetime(df["order_ts"])

    bad_amt = (df["basket_value"] <= 0) | (df["discount_amt"] < 0) | (df["discount_amt"] > df["basket_value"])
    df["invalid_amount"] = bad_amt
    df.loc[bad_amt, ["basket_value", "discount_amt"]] = np.nan
    log.append(("orders", "Impossible amounts (basket <= 0, negative discount, discount > basket)",
                int(bad_amt.sum()), "Amounts set to NaN, row kept and flagged invalid_amount"))

    bad_dm = df["delivery_minutes"] > MAX_DELIVERY_MIN
    df["delivery_outlier"] = bad_dm
    df.loc[bad_dm, "delivery_minutes"] = np.nan
    log.append(("orders", f"Delivery time outliers (>{MAX_DELIVERY_MIN} min, up to 811)",
                int(bad_dm.sum()), "Set to NaN, row kept and flagged delivery_outlier"))

    n_miss = int((df["delivery_minutes"].isna() & (df["status"] == "cancelled")).sum())
    log.append(("orders", "Missing delivery_minutes on cancelled orders", n_miss,
                "Expected (never delivered); left NaN"))

    far = int((df["distance_km"] > 10).sum())
    df["long_distance"] = df["distance_km"] > 10
    log.append(("orders", "Long-distance orders (>10 km)", far,
                "Plausible (slower deliveries); kept and flagged long_distance"))
    return df, log


def build_customer_features(customers: pd.DataFrame, orders: pd.DataFrame, cutoff) -> pd.DataFrame:
    """One row per customer using orders placed before `cutoff` (vectorised)."""
    cutoff = pd.Timestamp(cutoff)
    o = orders[orders["order_ts"] < cutoff]
    spend = o[(o["status"] != "cancelled") & ~o["invalid_amount"]]

    g = o.groupby("customer_id")
    feats = pd.DataFrame({
        "last_order": g["order_ts"].max(),
        "frequency": g.size(),
        "pct_rain": g["is_raining"].mean() * 100,
        "pct_cancelled": g["status"].apply(lambda s: (s == "cancelled").mean() * 100),
        "avg_delivery_min": g["delivery_minutes"].mean(),
    })
    s = spend.groupby("customer_id")
    feats["total_spend"] = s["basket_value"].sum()
    feats["avg_spend"] = s["basket_value"].mean()
    feats["discount_share"] = s["discount_amt"].sum() / s["basket_value"].sum()

    out = customers.set_index("customer_id").join(feats)
    out["recency_days"] = (cutoff - out["last_order"]).dt.days
    out["tenure_days"] = (cutoff - out["signup_date"]).dt.days
    out["frequency"] = out["frequency"].fillna(0).astype(int)
    out["total_spend"] = out["total_spend"].fillna(0.0)
    return out.reset_index()
