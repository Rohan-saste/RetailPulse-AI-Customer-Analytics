# ============================================================
# RetailPulse - Phase 5: Feature Engineering
# Notebook: 04_feature_engineering.ipynb
# ============================================================

import pandas as pd
import numpy as np

df = pd.read_csv("../data/processed/clean_retail_data.csv", parse_dates=['InvoiceDate'])

# Create all features
df['Revenue']  = df['Quantity'] * df['Price']       # Sale amount per row
df['Year']     = df['InvoiceDate'].dt.year           # 2009, 2010, 2011
df['Month']    = df['InvoiceDate'].dt.month          # 1-12
df['Day']      = df['InvoiceDate'].dt.day            # 1-31
df['Weekday']  = df['InvoiceDate'].dt.dayofweek     # 0=Monday, 6=Sunday
df['Hour']     = df['InvoiceDate'].dt.hour           # 0-23
df['Quarter']  = df['InvoiceDate'].dt.quarter        # 1-4

print("✅ Features created:")
print(df[['Revenue','Year','Month','Day','Weekday','Hour','Quarter']].head())

df.to_csv("../data/processed/featured_data.csv", index=False)
print("\n✅ Saved: featured_data.csv")


# ============================================================
# RetailPulse - Phase 6: Customer Segmentation (RFM + KMeans)
# Notebook: 05_customer_segmentation.ipynb
# ============================================================

import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import warnings
warnings.filterwarnings('ignore')

plt.rcParams['figure.figsize'] = (12, 6)
IMAGES_PATH = "../images/"

# ── Step 1: Calculate RFM ────────────────────────────────────
"""
RFM Analysis:
- R (Recency)   : Customer ne kitne diwas aadhi last purchase kela
- F (Frequency) : Customer ne total kitne wela purchase kela
- M (Monetary)  : Customer ne total kitne paise kharch kele

He tin metrics milun customer che value kalte
"""
snapshot_date = df['InvoiceDate'].max() + pd.Timedelta(days=1)

rfm = df.groupby('Customer ID').agg({
    'InvoiceDate' : lambda x: (snapshot_date - x.max()).days,  # Recency
    'Invoice'     : 'nunique',                                   # Frequency
    'Revenue'     : 'sum'                                        # Monetary
}).reset_index()

rfm.columns = ['Customer ID', 'Recency', 'Frequency', 'Monetary']

print("✅ RFM Calculated:")
print(rfm.describe())


# ── Step 2: Scale the Data ───────────────────────────────────
"""
STANDARDIZATION:
- RFM values different scales madhe astat (Recency: days, Monetary: pounds)
- KMeans sathi sagle values same scale la aane garajecha
- StandardScaler → mean=0, std=1 banawato
"""
scaler = StandardScaler()
rfm_scaled = scaler.fit_transform(rfm[['Recency', 'Frequency', 'Monetary']])


# ── Step 3: Elbow Method ─────────────────────────────────────
"""
ELBOW METHOD:
- Optimal number of clusters select karnya sathi
- Inertia (within-cluster sum of squares) plot karto
- Jya point la elbow dikhto tyach k value best hoti
"""
inertias = []
K_range = range(2, 11)

for k in K_range:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(rfm_scaled)
    inertias.append(kmeans.inertia_)

plt.figure(figsize=(10, 5))
plt.plot(K_range, inertias, 'bo-', linewidth=2, markersize=8)
plt.axvline(x=4, color='red', linestyle='--', label='Optimal K=4')
plt.title("Elbow Method – Optimal Number of Clusters", fontweight='bold')
plt.xlabel("Number of Clusters (K)")
plt.ylabel("Inertia (WCSS)")
plt.legend()
plt.tight_layout()
plt.savefig(f"{IMAGES_PATH}11_elbow_method.png", dpi=150)
plt.show()
print("📌 Insight: K=4 or K=5 optimal ahe (elbow point)")


# ── Step 4: Apply KMeans with K=4 ───────────────────────────
kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
rfm['Cluster'] = kmeans.fit_predict(rfm_scaled)


# ── Step 5: Assign Business Labels ──────────────────────────
"""
CLUSTER LABELS:
- RFM values cha basis var clusters la business names deto
- Monetary madhe highest = Premium
- Recency kam ani Frequency jast = Loyal
- etc.
"""
cluster_summary = rfm.groupby('Cluster')[['Recency','Frequency','Monetary']].mean().round(1)
print("\n📊 Cluster Summary:")
print(cluster_summary)

# Auto-assign labels based on Monetary ranking
cluster_monetary = rfm.groupby('Cluster')['Monetary'].mean().sort_values(ascending=False)
labels = {
    cluster_monetary.index[0]: 'Premium Customers',
    cluster_monetary.index[1]: 'Loyal Customers',
    cluster_monetary.index[2]: 'Regular Customers',
    cluster_monetary.index[3]: 'At Risk Customers',
}
rfm['Segment'] = rfm['Cluster'].map(labels)

print("\n👥 Segment Counts:")
print(rfm['Segment'].value_counts())


# ── Step 6: Visualize Clusters ──────────────────────────────
plt.figure(figsize=(12, 5))

# Scatter: Recency vs Monetary
plt.subplot(1, 2, 1)
colors = {'Premium Customers': '#2ecc71', 'Loyal Customers': '#3498db',
          'Regular Customers': '#f39c12', 'At Risk Customers': '#e74c3c'}
for seg, grp in rfm.groupby('Segment'):
    plt.scatter(grp['Recency'], grp['Monetary'], label=seg,
                alpha=0.5, color=colors[seg], s=30)
plt.title("Customer Segments: Recency vs Monetary", fontweight='bold')
plt.xlabel("Recency (days)")
plt.ylabel("Monetary (£)")
plt.legend(fontsize=9)

# Bar: Segment distribution
plt.subplot(1, 2, 2)
seg_counts = rfm['Segment'].value_counts()
plt.bar(seg_counts.index, seg_counts.values,
        color=[colors[s] for s in seg_counts.index])
plt.title("Customer Count per Segment", fontweight='bold')
plt.ylabel("Number of Customers")
plt.xticks(rotation=20, ha='right')

plt.tight_layout()
plt.savefig(f"{IMAGES_PATH}12_customer_segments.png", dpi=150)
plt.show()


# ── Step 7: Save Customer Segments ──────────────────────────
rfm.to_csv("../data/processed/customer_segments.csv", index=False)
print("\n✅ Saved: customer_segments.csv")
print("➡️  Next: Open 06_demand_forecasting.ipynb")
