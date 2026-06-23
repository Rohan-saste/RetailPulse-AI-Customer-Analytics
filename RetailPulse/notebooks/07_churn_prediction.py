# ============================================================
# RetailPulse - Phase 8: Customer Churn Prediction
# Notebook: 07_churn_prediction.ipynb
# ============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (accuracy_score, precision_score, recall_score,
                             f1_score, roc_auc_score, confusion_matrix,
                             classification_report)
import warnings
warnings.filterwarnings('ignore')

IMAGES_PATH = "../images/"
plt.rcParams['figure.figsize'] = (12, 5)


# ── Step 1: Load & Create Churn Label ────────────────────────
"""
CHURN DEFINITION:
- Customer ne last 90 diwsaat purchase kele nahi → Churn = 1
- Customer ne last 90 diwsaat purchase kele      → Churn = 0
- He retail industry madhe standard definition ahe
"""
df = pd.read_csv("../data/processed/clean_retail_data.csv", parse_dates=['InvoiceDate'])
df['Revenue'] = df['Quantity'] * df['Price']

snapshot_date = df['InvoiceDate'].max() + pd.Timedelta(days=1)

# RFM features
cust = df.groupby('Customer ID').agg(
    Recency    = ('InvoiceDate', lambda x: (snapshot_date - x.max()).days),
    Frequency  = ('Invoice', 'nunique'),
    Monetary   = ('Revenue', 'sum'),
    AvgRevenue = ('Revenue', 'mean'),
    TotalItems = ('Quantity', 'sum'),
    AvgQuantity= ('Quantity', 'mean'),
).reset_index()

# Churn label: 90 days naahi visit kela → churned
cust['Churn'] = (cust['Recency'] > 90).astype(int)

print(f"✅ Churn dataset created: {len(cust):,} customers")
print(f"   Churned     : {cust['Churn'].sum():,} ({cust['Churn'].mean()*100:.1f}%)")
print(f"   Not Churned : {(cust['Churn']==0).sum():,} ({(cust['Churn']==0).mean()*100:.1f}%)")


# ── Step 2: Features & Target Split ─────────────────────────
features = ['Recency', 'Frequency', 'Monetary', 'AvgRevenue', 'TotalItems', 'AvgQuantity']
X = cust[features]
y = cust['Churn']

# ── Step 3: Train-Test Split (80-20) ────────────────────────
"""
TRAIN-TEST SPLIT:
- 80% data → model train karnya sathi
- 20% data → model test karnya sathi
- random_state=42 → reproducibility sathi (same results milat rahtil)
"""
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
print(f"\n✅ Train set: {X_train.shape[0]:,} | Test set: {X_test.shape[0]:,}")


# ── Step 4: Scale Features ───────────────────────────────────
scaler = StandardScaler()
X_train_sc = scaler.fit_transform(X_train)
X_test_sc  = scaler.transform(X_test)


# ── Step 5: Train Multiple Models ───────────────────────────
models = {
    'Logistic Regression' : LogisticRegression(random_state=42, max_iter=500),
    'Decision Tree'       : DecisionTreeClassifier(random_state=42, max_depth=5),
    'Random Forest'       : RandomForestClassifier(random_state=42, n_estimators=100, n_jobs=-1),
}

try:
    from xgboost import XGBClassifier
    models['XGBoost'] = XGBClassifier(random_state=42, eval_metric='logloss', verbosity=0)
except ImportError:
    print("⚠️  XGBoost not installed - skipping")

# ── Step 6: Evaluate All Models ─────────────────────────────
results = {}
for name, model in models.items():
    model.fit(X_train_sc, y_train)
    y_pred = model.predict(X_test_sc)
    y_prob = model.predict_proba(X_test_sc)[:, 1]

    results[name] = {
        'Accuracy' : accuracy_score(y_test, y_pred),
        'Precision': precision_score(y_test, y_pred),
        'Recall'   : recall_score(y_test, y_pred),
        'F1 Score' : f1_score(y_test, y_pred),
        'ROC-AUC'  : roc_auc_score(y_test, y_prob),
    }
    print(f"\n✅ {name} trained")

# ── Step 7: Comparison Table ─────────────────────────────────
results_df = pd.DataFrame(results).T.round(4)
print("\n📊 MODEL COMPARISON:")
print(results_df.to_string())


# ── Step 8: Best Model & Confusion Matrix ───────────────────
best_model_name = results_df['F1 Score'].idxmax()
print(f"\n🏆 Best Model: {best_model_name}")
print("   (F1 Score highest ahe - Precision ani Recall cha balance)")

best_model = models[best_model_name]
y_pred_best = best_model.predict(X_test_sc)

cm = confusion_matrix(y_test, y_pred_best)
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=['Not Churned', 'Churned'],
            yticklabels=['Not Churned', 'Churned'])
plt.title(f"Confusion Matrix – {best_model_name}", fontweight='bold')
plt.ylabel("Actual")
plt.xlabel("Predicted")
plt.tight_layout()
plt.savefig(f"{IMAGES_PATH}15_confusion_matrix.png", dpi=150)
plt.show()


# ── Step 9: Feature Importance ──────────────────────────────
if hasattr(best_model, 'feature_importances_'):
    fi = pd.Series(best_model.feature_importances_, index=features).sort_values(ascending=True)
    plt.figure(figsize=(10, 5))
    fi.plot(kind='barh', color='steelblue')
    plt.title("Feature Importance", fontweight='bold')
    plt.xlabel("Importance Score")
    plt.tight_layout()
    plt.savefig(f"{IMAGES_PATH}16_feature_importance.png", dpi=150)
    plt.show()
    print("📌 Insight: Recency saglya important feature ahe churn prediction sathi")


# ── Step 10: Save Results ────────────────────────────────────
import pickle
with open("../models/best_churn_model.pkl", "wb") as f:
    pickle.dump(best_model, f)

with open("../models/scaler.pkl", "wb") as f:
    pickle.dump(scaler, f)

cust.to_csv("../data/processed/churn_data.csv", index=False)

print("\n✅ Saved: best_churn_model.pkl, scaler.pkl, churn_data.csv")
print("➡️  Next: Open dashboard/app.py for Streamlit Dashboard")
