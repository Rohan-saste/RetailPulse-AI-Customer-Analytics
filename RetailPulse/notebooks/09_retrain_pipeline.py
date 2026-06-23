# ============================================================
# RetailPulse - Phase 11: Retraining & Orcheration Pipeline
# File: notebooks/09_retrain_pipeline.py
# ============================================================

import subprocess
import os
import sys

def run_script(script_name, base_dir):
    script_path = os.path.join(base_dir, script_name)
    print(f"\n[RUNNING] Running Pipeline Step: {script_name}...")
    
    # Run python script using the same executable environment with UTF-8 encoding forced
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    res = subprocess.run([sys.executable, script_path], cwd=base_dir, env=env)
    if res.returncode == 0:
        print(f"[SUCCESS] Step {script_name} completed successfully!")
        return True
    else:
        print(f"[ERROR] Step {script_name} failed with exit code: {res.returncode}")
        return False

def trigger_pipeline():
    print("=" * 60)
    print("  RetailPulse Automated Retraining Pipeline Triggered")
    print("=" * 60)
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    pipeline_steps = [
        "02_data_cleaning.py",
        "04_05_segmentation.py",
        "06_demand_forecasting.py",
        "07_churn_prediction.py",
        "08_mlops_monitoring.py"
    ]
    
    for step in pipeline_steps:
        success = run_script(step, base_dir)
        if not success:
            print("\n[ERROR] Pipeline execution terminated due to errors.")
            return False
            
    print("\n[SUCCESS] Pipeline Execution Completed Successfully!")
    print("=" * 60)
    return True

if __name__ == "__main__":
    trigger_pipeline()
