from typing import List
import pandas as pd
import numpy as np
import os
import json
from datetime import timedelta
from joblib import load
from app.deps import get_orders_df
from app.config import settings

_MODEL = None
_META = None

def _try_load_model():
    global _MODEL, _META
    if _MODEL is not None and _META is not None:
        return
    model_path = os.path.join(settings.models_dir, "demand_lgbm.joblib")
    meta_path = os.path.join(settings.models_dir, "demand_lgbm_meta.json")
    if os.path.exists(model_path) and os.path.exists(meta_path):
        _MODEL = load(model_path)
        with open(meta_path) as f:
            _META = json.load(f)

def _seasonal_baseline(series: pd.Series, horizon: int) -> List[float]:
    if len(series) >= 7:
        last_week = series.iloc[-7:].values
        reps = int(np.ceil(horizon / 7))
        pred = np.tile(last_week, reps)[:horizon]
    else:
        mean_val = float(series.mean() if len(series) else 1.0)
        pred = [mean_val] * horizon
    return [float(x) for x in pred]

def _build_supervised_row(sku: str, region: str, dow: int, feature_cols: list) -> pd.DataFrame:
    base = {"dow": dow}
    df = pd.DataFrame([base])

    for col in feature_cols:
        if col.startswith("sku_"):
            df[col] = 1 if col == f"sku_{sku}" else 0
        elif col.startswith("region_"):
            df[col] = 1 if col == f"region_{region}" else 0

    for col in feature_cols:
        if col not in df.columns:
            df[col] = 0
    df = df[feature_cols]
    return df

def forecast_sku_region(sku: str, region: str, horizon_days: int = 7) -> List[float]:
    df = get_orders_df().copy()
    df["created_at"] = pd.to_datetime(df["created_at"])
    series = (
        df[(df["sku"] == sku) & ((df["region"] == region) | df["region"].isna())]
        .groupby(df["created_at"].dt.date)["qty"]
        .sum()
        .astype(float)
        .reset_index(drop=True)
    )

    # try ML model first
    _try_load_model()
    if _MODEL is not None and _META is not None:
        feature_cols = _META.get("feature_cols", [])
        preds = []

        start = (df["created_at"].max().date() if not df.empty else pd.Timestamp.today().date())
        for i in range(1, horizon_days + 1):
            day = pd.Timestamp(start) + pd.Timedelta(days=i)
            dow = int(day.dayofweek)
            X_row = _build_supervised_row(sku, region, dow, feature_cols)
            y_hat = float(_MODEL.predict(X_row)[0])
            preds.append(max(y_hat, 0.0))
        return preds

    # fallback
    return _seasonal_baseline(series, horizon_days)
