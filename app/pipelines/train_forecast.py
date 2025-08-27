import argparse
import pandas as pd
from lightgbm import LGBMRegressor
import json
from joblib import dump
import os

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    df = pd.read_parquet(args.data)
    df["dow"] = pd.to_datetime(df["date"]).dt.dayofweek
    X = pd.get_dummies(df[["dow", "sku", "region"]], columns=["sku", "region"])
    y = df["demand"].astype(float)

    model = LGBMRegressor(n_estimators=200)
    model.fit(X, y)

    feature_cols = list(X.columns)

    # save model
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    model_path = args.out.replace(".txt", ".joblib")
    dump(model, model_path)

    # save feature schema (columns)
    meta = {"feature_cols": feature_cols}
    with open(args.out.replace(".txt", "_meta.json"), "w") as f:
        json.dump(meta, f)

    print(f"model saved to {model_path}")
    print(f"feature meta saved to {args.out.replace('.txt', '_meta.json')}")

if __name__ == "__main__":
    main()
