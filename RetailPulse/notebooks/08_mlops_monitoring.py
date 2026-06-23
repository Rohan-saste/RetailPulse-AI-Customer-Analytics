# ============================================================
# RetailPulse - Phase 10: MLOps Monitoring & Drift Detection
# File: notebooks/08_mlops_monitoring.py
# ============================================================

import pandas as pd
import numpy as np
import os
import json
from scipy.stats import ks_2samp

def run_drift_analysis():
    print("⏳ Starting Data Drift Analysis...")
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_dir, "../../RetailPulse/data/processed/clean_retail_data.csv")
    output_path = os.path.join(base_dir, "../../RetailPulse/data/processed/drift_report.json")
    
    if not os.path.exists(data_path):
        print("❌ Clean retail data not found. Run cleaning script first.")
        return
        
    df = pd.read_csv(data_path, parse_dates=['InvoiceDate'])
    
    # Split data into reference (2009-2010) and current (2010-2011) to check for temporal drift
    df_ref = df[df['InvoiceDate'] < '2010-12-01']
    df_curr = df[df['InvoiceDate'] >= '2010-12-01']
    
    if len(df_ref) == 0 or len(df_curr) == 0:
        print("❌ Insufficient data in reference or current partition to evaluate drift.")
        return
        
    drift_report = {
        "status": "Success",
        "reference_period": f"{df_ref['InvoiceDate'].min().date()} to {df_ref['InvoiceDate'].max().date()}",
        "reference_rows": len(df_ref),
        "current_period": f"{df_curr['InvoiceDate'].min().date()} to {df_curr['InvoiceDate'].max().date()}",
        "current_rows": len(df_curr),
        "metrics": {}
    }
    
    # Run Kolmogorov-Smirnov test on numerical features
    features = ['Quantity', 'Price', 'Revenue']
    drift_detected_global = False
    
    for feat in features:
        ref_values = df_ref[feat]
        curr_values = df_curr[feat]
        
        stat, p_val = ks_2samp(ref_values, curr_values)
        drift_detected = p_val < 0.05  # 95% confidence threshold
        if drift_detected:
            drift_detected_global = True
            
        drift_report["metrics"][feat] = {
            "ks_statistic": round(float(stat), 5),
            "p_value": float(p_val),
            "drift_detected": bool(drift_detected),
            "ref_mean": round(float(ref_values.mean()), 3),
            "curr_mean": round(float(curr_values.mean()), 3)
        }
        
    drift_report["drift_detected"] = drift_detected_global
    
    # Save the report as JSON
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(drift_report, f, indent=4)
        
    print("✅ Drift Analysis Complete!")
    print(f"   Drift Detected: {drift_report['drift_detected']}")
    print(f"   Report Saved to: {output_path}")

if __name__ == "__main__":
    run_drift_analysis()
