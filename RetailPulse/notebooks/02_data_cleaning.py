# ============================================================
# RetailPulse - Phase 3: Data Cleaning
# Notebook: 02_data_cleaning.ipynb
# ============================================================

# ── CELL 1 ── Imports & Load Merged Data ─────────────────────
import pandas as pd
import numpy as np
import os

# Load merged data (Phase 2 madhe merge kela hota)
DATA_PATH = "../data/raw/online_retail_II.xlsx"

df1 = pd.read_excel(DATA_PATH, sheet_name='Year 2009-2010', engine='openpyxl')
df2 = pd.read_excel(DATA_PATH, sheet_name='Year 2010-2011', engine='openpyxl')
df = pd.concat([df1, df2], ignore_index=True)

print(f"✅ Data Loaded: {df.shape[0]:,} rows")


# ── CELL 2 ── Before Cleaning Summary ────────────────────────
print("📊 BEFORE CLEANING:")
print(f"   Total Rows     : {df.shape[0]:,}")
print(f"   Null Values    : {df.isnull().sum().sum():,}")
print(f"   Duplicates     : {df.duplicated().sum():,}")


# ── CELL 3 ── Step 1: Remove Null Customer IDs ───────────────
"""
WHY?
- Customer ID naste tar customer kon ahe te kalat nahi
- Segmentation ani Churn sathi Customer ID garajecha aahe
- म्हणून null Customer ID rows remove karto
"""
before = len(df)
df = df.dropna(subset=['Customer ID'])
after = len(df)
print(f"✅ Step 1 - Removed Null Customer IDs: {before - after:,} rows removed")


# ── CELL 4 ── Step 2: Remove Duplicates ──────────────────────
"""
WHY?
- Same data 2 wela asel tar analysis chukichi hote
- Duplicate rows remove karne garajecha
"""
before = len(df)
df = df.drop_duplicates()
after = len(df)
print(f"✅ Step 2 - Removed Duplicates: {before - after:,} rows removed")


# ── CELL 5 ── Step 3: Remove Cancelled Invoices ──────────────
"""
WHY?
- Cancelled invoices = returns/refunds
- Invoice number 'C' ne suru hote (e.g., C536379)
- Sales analysis sathi cancelled orders nako asato
"""
before = len(df)
df = df[~df['Invoice'].astype(str).str.startswith('C')]
after = len(df)
print(f"✅ Step 3 - Removed Cancelled Invoices: {before - after:,} rows removed")


# ── CELL 6 ── Step 4: Remove Negative Quantity ───────────────
"""
WHY?
- Quantity negative asu shakat nahi (e.g., -5 products sold?)
- He returns/errors astat
- Positive quantity aste tevhach sale valid aaste
"""
before = len(df)
df = df[df['Quantity'] > 0]
after = len(df)
print(f"✅ Step 4 - Removed Negative Quantity: {before - after:,} rows removed")


# ── CELL 7 ── Step 5: Remove Zero/Negative Price ─────────────
"""
WHY?
- Price 0 ya negative asu shakat nahi
- He data entry errors astat
- Revenue calculate karnya sathi positive price garajecha
"""
before = len(df)
df = df[df['Price'] > 0]
after = len(df)
print(f"✅ Step 5 - Removed Zero/Negative Price: {before - after:,} rows removed")


# ── CELL 8 ── Step 6: Convert InvoiceDate to Datetime ────────
"""
WHY?
- InvoiceDate abhi 'object' (text) format madhe aahe
- Date operations (month, year, weekday) sathi datetime format garajecha
- pd.to_datetime() → text to date convert karto
"""
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
print(f"✅ Step 6 - InvoiceDate converted to: {df['InvoiceDate'].dtype}")


# ── CELL 9 ── Step 7: Create Revenue Column ──────────────────
"""
WHY?
- Revenue = Quantity × Price
- He saglyana mahit aste pan dataset madhe nahi hote
- Revenue column analytics sathi saglya aahe important feature ahe
"""
df['Revenue'] = df['Quantity'] * df['Price']
print(f"✅ Step 7 - Revenue column created!")
print(f"   Total Revenue: £{df['Revenue'].sum():,.2f}")


# ── CELL 10 ── Step 8: Customer ID as Integer ────────────────
"""
WHY?
- Customer ID float (17850.0) as aasto
- Integer (17850) as store karna clean ahe
"""
df['Customer ID'] = df['Customer ID'].astype(int)
print(f"✅ Step 8 - Customer ID converted to integer")


# ── CELL 11 ── After Cleaning Summary ────────────────────────
print("\n📊 AFTER CLEANING:")
print(f"   Total Rows      : {df.shape[0]:,}")
print(f"   Total Columns   : {df.shape[1]}")
print(f"   Null Values     : {df.isnull().sum().sum():,}")
print(f"   Unique Customers: {df['Customer ID'].nunique():,}")
print(f"   Unique Products : {df['StockCode'].nunique():,}")
print(f"   Countries       : {df['Country'].nunique():,}")
print(f"   Date Range      : {df['InvoiceDate'].min().date()} to {df['InvoiceDate'].max().date()}")
print(f"   Total Revenue   : £{df['Revenue'].sum():,.2f}")


# ── CELL 12 ── Save Cleaned Data ─────────────────────────────
"""
SAVE:
- Cleaned data 'data/processed/' folder madhe save karto
- CSV format madhe save karto (universal format)
- Future phases madhe he directly load karto
"""
OUTPUT_PATH = "../data/processed/clean_retail_data.csv"
df.to_csv(OUTPUT_PATH, index=False)
print(f"\n✅ Cleaned data saved to: {OUTPUT_PATH}")
print("➡️  Next: Open 03_eda.ipynb")
