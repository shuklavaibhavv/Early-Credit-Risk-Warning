"""
Project Launcher Script for Credit Risk Quantitative Analysis.

1. Runs end-to-end credit modeling pipeline via src/run_pipeline.py.
2. Validates output dataset generation.
3. Automatically launches the interactive dashboard (Streamlit or static HTML/JS via webbrowser).
"""

import sys
import subprocess
import webbrowser
from pathlib import Path

# Add src directory to Python Path
project_dir = Path(__file__).parent
src_dir = project_dir / "src"
sys.path.insert(0, str(src_dir))

from run_pipeline import main as run_pipeline_main


def start():
    print("=" * 80)
    print("LAUNCHING CREDIT RISK PROJECT ENGINE")
    print("=" * 80)

    # 1. Run full pipeline
    try:
        pipeline_success = run_pipeline_main()
    except Exception as e:
        print("\n" + "!" * 80)
        print(f"PIPELINE FAILURE DETECTED: {e}")
        print("Dashboard launch aborted.")
        print("!" * 80)
        sys.exit(1)

    # 2. Check for final scored CSV
    final_csv = project_dir / "data" / "composite_credit_scores.csv"

    if not final_csv.exists() or final_csv.stat().st_size == 0:
        print("\n" + "!" * 80)
        print("ERROR: Scored CSV file missing or empty after pipeline run.")
        print("Dashboard launch aborted.")
        print("!" * 80)
        sys.exit(1)

    print("\n" + "=" * 80)
    print("PIPELINE VERIFIED CLEAN. OPENING DASHBOARD...")
    print("=" * 80)

    dashboard_html = project_dir / "dashboard" / "index.html"
    dashboard_app = project_dir / "dashboard" / "app.py"

    # Check if streamlit is installed in python environment
    streamlit_installed = False
    try:
        import streamlit
        streamlit_installed = True
    except ImportError:
        streamlit_installed = False

    # 3. Automatically open dashboard (Streamlit app if available, else static HTML in default browser)
    if streamlit_installed and dashboard_app.exists():
        print(f"Launching Streamlit application: {dashboard_app}")
        try:
            subprocess.run(["streamlit", "run", str(dashboard_app)], check=True)
        except Exception as e:
            print(f"Streamlit launch encountered: {e}. Falling back to web browser...")
            webbrowser.open(f"file://{dashboard_html.resolve()}")
    elif dashboard_html.exists():
        print(f"Opening interactive HTML dashboard in default web browser: {dashboard_html}")
        webbrowser.open(f"file://{dashboard_html.resolve()}")
    else:
        print("Error: No dashboard file found in dashboard/ directory.")


if __name__ == "__main__":
    start()
