"""
========================================
RetailPulse - Project Setup Script
Phase 1: Project Structure Creation
========================================
"""

import os

# Project root folder name
PROJECT_NAME = "RetailPulse"

# All folders with their purpose
folders = {
    "data/raw"          : "Original dataset files - kabhi bhi edit karu naka",
    "data/processed"    : "Cleaned & processed data save hote ithe",
    "notebooks"         : "Jupyter Notebooks - EDA, Models, Analysis",
    "models"            : "Trained ML models (.pkl files) save hote ithe",
    "dashboard"         : "Streamlit dashboard files",
    "reports"           : "Final project report (PDF/Word)",
    "presentation"      : "PowerPoint presentation slides",
    "images"            : "Sagle charts ani graphs save hote ithe",
    "app"               : "Web app files (optional)",
}

print("=" * 50)
print("  RetailPulse - Project Setup Starting...")
print("=" * 50)

# Create each folder
for folder, purpose in folders.items():
    path = os.path.join(PROJECT_NAME, folder)
    os.makedirs(path, exist_ok=True)
    print(f"\n✅ Created : {path}")
    print(f"   Purpose  : {purpose}")

print("\n" + "=" * 50)
print("🎉 Project structure created successfully!")
print("=" * 50)
print("\n📌 Next Steps:")
print("  1. Place 'online_retail_II.xlsx' in data/raw/")
print("  2. Run: pip install -r requirements.txt")
print("  3. Open JupyterLab: jupyter lab")
print("  4. Start with: notebooks/01_data_loading.ipynb")
