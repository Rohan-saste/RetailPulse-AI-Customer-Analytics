# ============================================================
# RetailPulse - Phase 2: Data Loading
# Notebook: 01_data_loading.ipynb
# ============================================================
# Instructions: Copy each cell into a new Jupyter Notebook
# ============================================================

# ── CELL 1 ── Import Libraries ──────────────────────────────
"""
IMPORTS:
- pandas  → data handle karanya sathi (tables/dataframes)
- numpy   → mathematical operations sathi
- os      → file paths handle karanya sathi
"""
import pandas as pd
import numpy as np
import os

print("✅ All libraries imported successfully!")
print(f"   Pandas version  : {pd.__version__}")
print(f"   NumPy version   : {np.__version__}")


# ── CELL 2 ── Set File Paths ─────────────────────────────────
"""
FILE PATH:
- ithe tu dataset cha exact path deto
- raw data folder madhe file asel tar he kaam karte
"""
# Dataset path - apla data/raw/ folder madhe aahe
DATA_PATH = "../data/raw/online_retail_II.xlsx"

# Check if file exists
if os.path.exists(DATA_PATH):
    print(f"✅ Dataset found: {DATA_PATH}")
else:
    print(f"❌ Dataset NOT found at: {DATA_PATH}")
    print("   Please place 'online_retail_II.xlsx' in the data/raw/ folder")


# ── CELL 3 ── Load Both Excel Sheets ─────────────────────────
"""
EXCEL SHEETS:
- Year 2009-2010 → pehla sheet
- Year 2010-2011 → dusra sheet
- donhi sheets eka dataframe madhe merge karto
"""
print("⏳ Loading Excel file... (he thoda time gheto, wait kara)")

# Sheet 1: 2009-2010
df1 = pd.read_excel(DATA_PATH, sheet_name='Year 2009-2010', engine='openpyxl')
print(f"✅ Sheet 1 loaded: {df1.shape[0]:,} rows, {df1.shape[1]} columns")

# Sheet 2: 2010-2011
df2 = pd.read_excel(DATA_PATH, sheet_name='Year 2010-2011', engine='openpyxl')
print(f"✅ Sheet 2 loaded: {df2.shape[0]:,} rows, {df2.shape[1]} columns")

# Merge both sheets
df = pd.concat([df1, df2], ignore_index=True)
print(f"\n🎉 Merged Dataset: {df.shape[0]:,} rows, {df.shape[1]} columns")


# ── CELL 4 ── Dataset Shape ───────────────────────────────────
"""
SHAPE:
- shape → (rows, columns) dakhavato
- aplyala kitne records ahet he kalte
"""
print("📐 Dataset Shape:")
print(f"   Rows    : {df.shape[0]:,}")
print(f"   Columns : {df.shape[1]}")


# ── CELL 5 ── First 5 Rows (Head) ────────────────────────────
"""
HEAD:
- pehle 5 rows dakhavato
- data kasa dikhato he samajte
"""
print("\n👀 First 5 Rows (Head):")
df.head()


# ── CELL 6 ── Last 5 Rows (Tail) ─────────────────────────────
"""
TAIL:
- shevtache 5 rows dakhavato
- data properly load zala ka he check karto
"""
print("\n👀 Last 5 Rows (Tail):")
df.tail()


# ── CELL 7 ── Column Names ────────────────────────────────────
"""
COLUMNS:
- sagle column names dakhavato
- aplyala konte features (variables) ahet he samajte
"""
print("\n📋 Column Names:")
for i, col in enumerate(df.columns, 1):
    print(f"   {i}. {col}")


# ── CELL 8 ── Data Types ──────────────────────────────────────
"""
DTYPES (Data Types):
- pratyek column konata type ahe te dakhavato
- object → text/string
- int64  → integer number
- float64 → decimal number
- datetime64 → date & time
"""
print("\n🔢 Data Types:")
print(df.dtypes)


# ── CELL 9 ── Missing Values ──────────────────────────────────
"""
MISSING VALUES (Null Values):
- konata column madhe kitne values missing ahet te dakhavato
- Missing values = blank cells
- isnull() → True/False deto (null asel tar True)
- sum()    → True chi count karto
"""
print("\n❓ Missing Values per Column:")
missing = df.isnull().sum()
missing_pct = (missing / len(df) * 100).round(2)
missing_df = pd.DataFrame({
    'Missing Count': missing,
    'Missing %': missing_pct
})
print(missing_df[missing_df['Missing Count'] > 0])


# ── CELL 10 ── Duplicate Rows ─────────────────────────────────
"""
DUPLICATES:
- same data 2 wela asel tar to duplicate asto
- duplicate rows remove karne garajecha aste
"""
duplicates = df.duplicated().sum()
print(f"\n🔁 Duplicate Rows: {duplicates:,}")


# ── CELL 11 ── Statistical Summary ───────────────────────────
"""
DESCRIBE (Statistical Summary):
- numerical columns chi summary dakhavato
- count  → kitne values ahet
- mean   → average
- std    → standard deviation (spread)
- min    → minimum value
- max    → maximum value
- 25%/50%/75% → quartiles
"""
print("\n📊 Statistical Summary:")
df.describe()


# ── CELL 12 ── Save Raw Info ──────────────────────────────────
"""
INFO:
- sarvat important function
- sagle column names, data types, ani non-null counts eka jaghi dakhavato
"""
print("\n📝 Dataset Info:")
df.info()

print("\n✅ Phase 2 - Data Loading Complete!")
print("➡️  Next: Open 02_data_cleaning.ipynb")
