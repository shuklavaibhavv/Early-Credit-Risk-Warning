"""
End-to-End Credit Risk Pipeline Orchestrator.

Executes all core pipeline stages in sequence:
1. Batch ratio signal generation (Altman Z-Score, Debt/EBITDA, Interest Coverage, Current Ratio, Cash Burn).
2. Merton Distance-to-Default (DD) structural model calculations.
3. Composite Credit Risk Logistic Regression scoring model training and export.
4. Formal backtest quantification (Advance warning quarters & false positive checks).
"""

from pathlib import Path
from generate_ratio_signals import generate_ratio_signals
from generate_dtd_signals import run_dtd_analysis
from composite_score import train_composite_model
from backtest import run_backtest


def main():
    """Runs end-to-end credit risk modeling pipeline."""
    print("=" * 80)
    print("STARTING END-TO-END CREDIT RISK MODELING PIPELINE")
    print("=" * 80)

    # Stage 1: Financial Ratio Signals
    print("\n[Stage 1/4] Generating Financial Ratio Signals...")
    generate_ratio_signals()

    # Stage 2: Merton Distance-to-Default Structural Signals
    print("\n[Stage 2/4] Calculating Merton Distance-to-Default Signals...")
    run_dtd_analysis()

    # Stage 3: Composite Credit Risk Scoring Model
    print("\n[Stage 3/4] Training Composite Logistic Regression Model & Scoring Cohort...")
    train_composite_model()

    # Stage 4: Model Backtest & Validation
    print("\n[Stage 4/4] Executing Model Backtest & Advance Warning Metrics...")
    run_backtest()

    # Final Output Verification
    project_dir = Path(__file__).parent.parent
    final_csv = project_dir / "data" / "composite_credit_scores.csv"

    if final_csv.exists() and final_csv.stat().st_size > 0:
        print("\n" + "=" * 80)
        print("PIPELINE COMPLETED SUCCESSFULLY!")
        print(f"Final Scored Output: {final_csv}")
        print("=" * 80)
        return True
    else:
        raise RuntimeError(f"Pipeline finished but output CSV not found at {final_csv}")


if __name__ == "__main__":
    main()
