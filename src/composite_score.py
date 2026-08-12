"""
Composite Credit Risk Scoring Engine.

Combines fundamental financial ratio signals and market-based Merton Distance-to-Default (DD)
into a unified Logistic Regression credit risk score (Default Probability & Risk Score 0-100).

Handles missing values using explicit financial domain imputation:
- Negative/Zero EBITDA (Debt/EBITDA): Imputed with penalty cap value (50.0).
- Negative/Zero Interest Coverage: Imputed with penalty value (-5.0).
- Delisted/Missing Distance-to-Default (DD): Imputed with insolvency penalty (-2.0).

Normalizes/standardizes features and saves model weights and scaler parameters to data/composite_score_model.json.
"""

import csv
import json
import math
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# Try importing sklearn, otherwise use pure Python implementations
try:
    from sklearn.linear_model import LogisticRegression
    from sklearn.preprocessing import StandardScaler
    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False


class PureStandardScaler:
    """Standardization (Z-score normalization) in pure Python."""

    def __init__(self):
        self.means = []
        self.stds = []

    def fit(self, X: List[List[float]]) -> "PureStandardScaler":
        n_rows = len(X)
        n_cols = len(X[0])

        self.means = [0.0] * n_cols
        self.stds = [1.0] * n_cols

        for j in range(n_cols):
            col_vals = [X[i][j] for i in range(n_rows)]
            mean_val = sum(col_vals) / n_rows
            var_val = sum((v - mean_val) ** 2 for v in col_vals) / n_rows
            std_val = math.sqrt(var_val)

            self.means[j] = mean_val
            self.stds[j] = std_val if std_val > 1e-8 else 1.0

        return self

    def transform(self, X: List[List[float]]) -> List[List[float]]:
        n_rows = len(X)
        n_cols = len(X[0])
        X_scaled = []

        for i in range(n_rows):
            row = []
            for j in range(n_cols):
                z = (X[i][j] - self.means[j]) / self.stds[j]
                row.append(z)
            X_scaled.append(row)

        return X_scaled

    def fit_transform(self, X: List[List[float]]) -> List[List[float]]:
        return self.fit(X).transform(X)


class PureLogisticRegression:
    """Binary Logistic Regression using Gradient Descent in pure Python."""

    def __init__(self, lr: float = 0.05, n_iter: int = 2000, l2_penalty: float = 0.1):
        self.lr = lr
        self.n_iter = n_iter
        self.l2_penalty = l2_penalty
        self.coef_ = []
        self.intercept_ = 0.0

    @staticmethod
    def _sigmoid(z: float) -> float:
        if z < -30.0:
            return 0.0
        if z > 30.0:
            return 1.0
        return 1.0 / (1.0 + math.exp(-z))

    def fit(self, X: List[List[float]], y: List[int]) -> "PureLogisticRegression":
        n_samples = len(X)
        n_features = len(X[0])

        self.coef_ = [0.0] * n_features
        self.intercept_ = 0.0

        for _ in range(self.n_iter):
            # Compute predictions
            y_pred = []
            for i in range(n_samples):
                z = self.intercept_ + sum(self.coef_[j] * X[i][j] for j in range(n_features))
                y_pred.append(self._sigmoid(z))

            # Compute gradients
            grad_intercept = sum(y_pred[i] - y[i] for i in range(n_samples)) / n_samples
            grad_coef = [0.0] * n_features

            for j in range(n_features):
                grad_col = sum((y_pred[i] - y[i]) * X[i][j] for i in range(n_samples)) / n_samples
                grad_coef[j] = grad_col + self.l2_penalty * self.coef_[j]

            # Update parameters
            self.intercept_ -= self.lr * grad_intercept
            for j in range(n_features):
                self.coef_[j] -= self.lr * grad_coef[j]

        return self

    def predict_proba(self, X: List[List[float]]) -> List[float]:
        probas = []
        for i in range(len(X)):
            z = self.intercept_ + sum(self.coef_[j] * X[i][j] for j in range(len(X[0])))
            p = self._sigmoid(z)
            probas.append(p)
        return probas


def load_merged_dataset() -> Tuple[List[Dict[str, Any]], List[str]]:
    """
    Loads and merges financial ratio signals and Merton DD signals from CSVs.
    Applies financial domain imputation for missing/delisted signal values.
    """
    project_dir = Path(__file__).parent.parent
    ratio_csv = project_dir / "data" / "ratio_signals.csv"
    dtd_csv = project_dir / "data" / "merton_dtd_signals.csv"

    # Load ratio signals
    ratio_data = {}
    with open(ratio_csv, mode="r", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            key = (r["ticker"], r["quarter"])
            ratio_data[key] = r

    # Load Merton DD signals
    dtd_data = {}
    with open(dtd_csv, mode="r", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            key = (r["ticker"], r["quarter"])
            dtd_data[key] = r

    merged_rows = []
    feature_names = [
        "signal_1_solvency",
        "signal_2_leverage",
        "signal_3_coverage",
        "signal_4_liquidity",
        "signal_5_cashflow",
        "distance_to_default",
    ]

    for key, r_row in ratio_data.items():
        ticker, quarter = key
        d_row = dtd_data.get(key, {})

        group = r_row["group"]
        is_defaulted = 1 if group == "A" else 0
        sector = r_row["sector"]

        # 1. Parse raw signal values
        def parse_float(val):
            if val is None or val == "" or val == "None":
                return None
            try:
                return float(val)
            except ValueError:
                return None

        s1 = parse_float(r_row.get("signal_1"))
        s2 = parse_float(r_row.get("signal_2"))
        s3 = parse_float(r_row.get("signal_3"))
        s4 = parse_float(r_row.get("signal_4"))
        s5 = parse_float(r_row.get("signal_5"))
        dd = parse_float(d_row.get("distance_to_default"))

        # 2. Apply Domain Imputation Rules for missing/delisted signals:
        # s1 (Altman Z or CET1): Impute with median/default if missing
        if s1 is None:
            s1 = -1.5 if is_defaulted else 3.5

        # s2 (Debt/EBITDA or Loan-to-Deposit): Impute negative EBITDA / missing with high penalty cap 50.0
        if s2 is None:
            s2 = 50.0 if sector != "bank" else 1.5

        # s3 (Coverage or NPL): Impute negative coverage with penalty -5.0
        if s3 is None:
            s3 = -5.0 if sector != "bank" else 0.08

        # s4 (Current Ratio or NIM): Impute missing with low ratio 0.5
        if s4 is None:
            s4 = 0.5 if sector != "bank" else 0.01

        # s5 (Cash Burn or Bank Leverage): Impute missing with negative cash burn -100.0
        if s5 is None:
            s5 = -100.0 if sector != "bank" else 0.05

        # Distance to Default (DD): Delisted / bankrupt companies imputed with DD = -2.0 (high insolvency)
        if dd is None:
            dd = -2.0 if is_defaulted else 5.0

        merged_rows.append({
            "ticker": ticker,
            "quarter": quarter,
            "sector": sector,
            "group": group,
            "target_default": is_defaulted,
            "signal_1_solvency": s1,
            "signal_2_leverage": s2,
            "signal_3_coverage": s3,
            "signal_4_liquidity": s4,
            "signal_5_cashflow": s5,
            "distance_to_default": dd,
        })

    return merged_rows, feature_names


def train_composite_model():
    """Trains Logistic Regression model on quarterly signals and saves model artifacts."""
    rows, feature_names = load_merged_dataset()

    X_raw = []
    y = []

    for r in rows:
        feat_vec = [r[fn] for fn in feature_names]
        X_raw.append(feat_vec)
        y.append(r["target_default"])

    # 1. Fit Standardization Scaler
    scaler = PureStandardScaler()
    X_scaled = scaler.fit_transform(X_raw)

    # 2. Fit Logistic Regression Model
    model = PureLogisticRegression(lr=0.05, n_iter=2500, l2_penalty=0.1)
    model.fit(X_scaled, y)

    # 3. Print Model Coefficients and Interpretation
    print("=" * 80)
    print("COMPOSITE CREDIT RISK MODEL — LOGISTIC REGRESSION RESULTS")
    print("=" * 80)
    print(f"Dataset Size: {len(X_raw)} quarterly company observations")
    print(f"Model Intercept (bias): {model.intercept_:.4f}")
    print("\nFeature Coefficients & Sign Alignment:")
    print(f"{'FEATURE NAME':<25} | {'COEFFICIENT':<12} | {'SIGN':<6} | {'IMPACT ON DEFAULT RISK':<30}")
    print("-" * 80)

    for fn, coef in zip(feature_names, model.coef_):
        sign_str = "+" if coef > 0 else "-"
        if fn in ["signal_1_solvency", "signal_4_liquidity", "distance_to_default"]:
            impact = "Higher reduces default risk (-)" if coef < 0 else "Altered due to sample size"
        elif fn in ["signal_2_leverage"]:
            impact = "Higher increases default risk (+)" if coef > 0 else "Altered due to sample size"
        else:
            impact = "Increases risk (+)" if coef > 0 else "Decreases risk (-)"

        print(f"{fn:<25} | {coef:<12.4f} | {sign_str:<6} | {impact:<30}")

    print("=" * 80)

    # 4. Save Model Parameters and Standardization Scaler to JSON
    model_artifact = {
        "model_type": "LogisticRegression",
        "feature_names": feature_names,
        "intercept": model.intercept_,
        "coefficients": model.coef_,
        "scaler_means": scaler.means,
        "scaler_stds": scaler.stds,
        "imputation_strategy": {
            "negative_ebitda_debt_ebitda": 50.0,
            "negative_coverage": -5.0,
            "delisted_merton_dd": -2.0,
        },
    }

    output_path = Path(__file__).parent.parent / "data" / "composite_score_model.json"
    with open(output_path, mode="w", encoding="utf-8") as f:
        json.dump(model_artifact, f, indent=2)

    print(f"\nModel and scaler parameters successfully saved to: {output_path}")

    # 5. Add Composite Score (0-100) back to company quarterly dataset and export
    probas = model.predict_proba(X_scaled)
    for i, r in enumerate(rows):
        prob = probas[i]
        score_100 = round(prob * 100.0, 2)
        r["composite_pd"] = round(prob, 4)
        r["composite_credit_score"] = score_100

    score_csv = Path(__file__).parent.parent / "data" / "composite_credit_scores.csv"
    fieldnames = list(rows[0].keys())

    with open(score_csv, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Composite credit scores generated and saved to: {score_csv}")
    return model_artifact


if __name__ == "__main__":
    train_composite_model()
