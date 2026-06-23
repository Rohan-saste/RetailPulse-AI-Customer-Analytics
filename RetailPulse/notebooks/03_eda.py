# ============================================================
# RetailPulse - Phase 4: Exploratory Data Analysis (EDA)
# Notebook: 03_eda.ipynb
# ============================================================

# ── CELL 1 ── Imports ─────────────────────────────────────────
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# Professional chart style
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 12
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.titleweight'] = 'bold'
sns.set_theme(style="whitegrid", palette="muted")

IMAGES_PATH = "../images/"
import os; os.makedirs(IMAGES_PATH, exist_ok=True)

print("✅ All libraries imported!")


# ── CELL 2 ── Load Cleaned Data ──────────────────────────────
df = pd.read_csv("../data/processed/clean_retail_data.csv", parse_dates=['InvoiceDate'])

# Feature Engineering (basic - for EDA)
df['Year']    = df['InvoiceDate'].dt.year
df['Month']   = df['InvoiceDate'].dt.month
df['Day']     = df['InvoiceDate'].dt.day
df['Weekday'] = df['InvoiceDate'].dt.day_name()
df['Hour']    = df['InvoiceDate'].dt.hour

print(f"✅ Data Loaded: {df.shape[0]:,} rows")
df.head()


# ── CELL 3 ── Dataset Overview ────────────────────────────────
print("=" * 50)
print("  DATASET OVERVIEW")
print("=" * 50)
print(f"  Total Transactions : {df.shape[0]:,}")
print(f"  Unique Customers   : {df['Customer ID'].nunique():,}")
print(f"  Unique Products    : {df['StockCode'].nunique():,}")
print(f"  Countries          : {df['Country'].nunique()}")
print(f"  Total Revenue      : £{df['Revenue'].sum():,.2f}")
print(f"  Date Range         : {df['InvoiceDate'].min().date()} → {df['InvoiceDate'].max().date()}")
print("=" * 50)


# ── CELL 4 ── Chart 1: Top 10 Selling Products ───────────────
"""
BUSINESS INSIGHT:
- Kaun se products saglya jast biktat he kalto
- Inventory management ani procurement sathi useful
"""
top_products = df.groupby('Description')['Quantity'].sum().sort_values(ascending=False).head(10)

plt.figure(figsize=(14, 6))
bars = plt.barh(top_products.index[::-1], top_products.values[::-1], color='steelblue')
plt.title("Top 10 Best-Selling Products (by Quantity)", fontweight='bold')
plt.xlabel("Total Quantity Sold")
plt.ylabel("Product")
for bar, val in zip(bars, top_products.values[::-1]):
    plt.text(bar.get_width() + 500, bar.get_y() + bar.get_height()/2,
             f'{val:,}', va='center', fontsize=10)
plt.tight_layout()
plt.savefig(f"{IMAGES_PATH}01_top_selling_products.png", dpi=150)
plt.show()
print("📌 Insight: He products highest demand madhe ahet - stock priority dyave")


# ── CELL 5 ── Chart 2: Top 10 Revenue Products ───────────────
"""
BUSINESS INSIGHT:
- Revenue generate karnarya top products kalto
- Pricing strategy sathi important
"""
top_revenue = df.groupby('Description')['Revenue'].sum().sort_values(ascending=False).head(10)

plt.figure(figsize=(14, 6))
bars = plt.barh(top_revenue.index[::-1], top_revenue.values[::-1], color='darkorange')
plt.title("Top 10 Revenue-Generating Products", fontweight='bold')
plt.xlabel("Total Revenue (£)")
plt.ylabel("Product")
for bar, val in zip(bars, top_revenue.values[::-1]):
    plt.text(bar.get_width() + 100, bar.get_y() + bar.get_height()/2,
             f'£{val:,.0f}', va='center', fontsize=10)
plt.tight_layout()
plt.savefig(f"{IMAGES_PATH}02_top_revenue_products.png", dpi=150)
plt.show()
print("📌 Insight: Ye products business cha main revenue source ahet")


# ── CELL 6 ── Chart 3: Top 10 Countries by Revenue ──────────
"""
BUSINESS INSIGHT:
- Kaun te countries saglya jast revenue generate karto
- International expansion strategy sathi useful
"""
top_countries = df.groupby('Country')['Revenue'].sum().sort_values(ascending=False).head(10)

plt.figure(figsize=(12, 6))
sns.barplot(x=top_countries.values, y=top_countries.index, palette='Blues_r')
plt.title("Top 10 Countries by Revenue", fontweight='bold')
plt.xlabel("Total Revenue (£)")
plt.ylabel("Country")
plt.tight_layout()
plt.savefig(f"{IMAGES_PATH}03_top_countries.png", dpi=150)
plt.show()
print("📌 Insight: UK dominant market ahe. Netherlands, Ireland expansion opportunities ahet")


# ── CELL 7 ── Chart 4: Monthly Sales Trend ───────────────────
"""
BUSINESS INSIGHT:
- Sales konate mahinyat jast hoto te kalte
- Seasonality ani trends identify karto
"""
monthly = df.groupby(['Year', 'Month'])['Revenue'].sum().reset_index()
monthly['Period'] = pd.to_datetime(monthly[['Year', 'Month']].assign(DAY=1))

plt.figure(figsize=(14, 6))
plt.plot(monthly['Period'], monthly['Revenue'], marker='o', color='steelblue', linewidth=2)
plt.fill_between(monthly['Period'], monthly['Revenue'], alpha=0.15, color='steelblue')
plt.title("Monthly Revenue Trend (2009–2011)", fontweight='bold')
plt.xlabel("Month")
plt.ylabel("Revenue (£)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(f"{IMAGES_PATH}04_monthly_trend.png", dpi=150)
plt.show()
print("📌 Insight: November-December madhe sales peak hote - holiday season effect")


# ── CELL 8 ── Chart 5: Revenue by Day of Week ────────────────
"""
BUSINESS INSIGHT:
- Kaun te weekdays jast sales hoto
- Marketing campaigns schedule sathi useful
"""
weekday_order = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
weekday_rev = df.groupby('Weekday')['Revenue'].sum().reindex(weekday_order)

plt.figure(figsize=(10, 5))
sns.barplot(x=weekday_rev.index, y=weekday_rev.values, palette='coolwarm')
plt.title("Revenue by Day of Week", fontweight='bold')
plt.xlabel("Day")
plt.ylabel("Revenue (£)")
plt.tight_layout()
plt.savefig(f"{IMAGES_PATH}05_revenue_by_weekday.png", dpi=150)
plt.show()
print("📌 Insight: Thursday aani Wednesday la jast sales hoto")


# ── CELL 9 ── Chart 6: Revenue Distribution (Histogram) ──────
"""
BUSINESS INSIGHT:
- Revenue kase distribute ahe he kalte
- Outliers identify karto
"""
plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
df[df['Revenue'] < df['Revenue'].quantile(0.99)]['Revenue'].hist(bins=50, color='steelblue', edgecolor='white')
plt.title("Revenue Distribution", fontweight='bold')
plt.xlabel("Revenue (£)")
plt.ylabel("Count")

plt.subplot(1, 2, 2)
df[df['Quantity'] < df['Quantity'].quantile(0.99)]['Quantity'].hist(bins=50, color='coral', edgecolor='white')
plt.title("Quantity Distribution", fontweight='bold')
plt.xlabel("Quantity")
plt.ylabel("Count")

plt.tight_layout()
plt.savefig(f"{IMAGES_PATH}06_distributions.png", dpi=150)
plt.show()
print("📌 Insight: Right-skewed distribution - majority small orders, kahi large bulk orders")


# ── CELL 10 ── Chart 7: Top 10 Customers ─────────────────────
"""
BUSINESS INSIGHT:
- Top customers kaun ahet te kalte
- VIP customer program design karna sathi useful
"""
top_customers = df.groupby('Customer ID')['Revenue'].sum().sort_values(ascending=False).head(10)

plt.figure(figsize=(12, 5))
sns.barplot(x=top_customers.index.astype(str), y=top_customers.values, palette='viridis')
plt.title("Top 10 Customers by Revenue", fontweight='bold')
plt.xlabel("Customer ID")
plt.ylabel("Total Revenue (£)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(f"{IMAGES_PATH}07_top_customers.png", dpi=150)
plt.show()
print("📌 Insight: Top 10 customers significant revenue contribute kartat - VIP treatment dyave")


# ── CELL 11 ── Chart 8: Orders per Month ─────────────────────
monthly_orders = df.groupby(['Year','Month'])['Invoice'].nunique().reset_index()
monthly_orders['Period'] = pd.to_datetime(monthly_orders[['Year','Month']].assign(DAY=1))

plt.figure(figsize=(14, 5))
plt.bar(monthly_orders['Period'], monthly_orders['Invoice'], color='teal', width=20)
plt.title("Number of Orders per Month", fontweight='bold')
plt.xlabel("Month")
plt.ylabel("Number of Orders")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(f"{IMAGES_PATH}08_orders_per_month.png", dpi=150)
plt.show()
print("📌 Insight: Orders trend revenue trend shee align ahe")


# ── CELL 12 ── Chart 9: Price Distribution Boxplot ───────────
plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
df[df['Price'] < df['Price'].quantile(0.99)].boxplot(column='Price')
plt.title("Price Distribution (Boxplot)", fontweight='bold')

plt.subplot(1, 2, 2)
df[df['Revenue'] < df['Revenue'].quantile(0.99)].boxplot(column='Revenue')
plt.title("Revenue Distribution (Boxplot)", fontweight='bold')

plt.tight_layout()
plt.savefig(f"{IMAGES_PATH}09_boxplots.png", dpi=150)
plt.show()
print("📌 Insight: Outliers present ahet - cleaning madhe already handle kelele ahet")


# ── CELL 13 ── Chart 10: Correlation Heatmap ─────────────────
"""
BUSINESS INSIGHT:
- Numerical columns madhe correlation kalte
- Quantity ani Revenue strongly correlated asat
"""
numeric_cols = ['Quantity', 'Price', 'Revenue']
corr = df[numeric_cols].corr()

plt.figure(figsize=(8, 5))
sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm',
            square=True, linewidths=0.5)
plt.title("Correlation Heatmap", fontweight='bold')
plt.tight_layout()
plt.savefig(f"{IMAGES_PATH}10_correlation_heatmap.png", dpi=150)
plt.show()
print("📌 Insight: Quantity-Revenue madhe strong positive correlation ahe (expected)")


print("\n✅ Phase 4 - EDA Complete!")
print(f"   All charts saved in: {IMAGES_PATH}")
print("➡️  Next: Open 04_feature_engineering.ipynb")
