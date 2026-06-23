# ==============================================================
# RetailPulse Server – Data Service (CSV Loading & Analytics)
# ==============================================================
# Ports all data loading and aggregation logic from the original
# Streamlit dashboard (dashboard/app.py) into a reusable service.
# ==============================================================

import os
import json
import pandas as pd
import numpy as np
from typing import Optional, List, Dict, Any
from datetime import date
from app.config import settings
from app.utils.logger import logger


class DataService:
    """Singleton service that loads CSV data at startup and provides filtered analytics."""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self.df: Optional[pd.DataFrame] = None
        self.segments: Optional[pd.DataFrame] = None
        self.forecast: Optional[pd.DataFrame] = None
        self.churn_df: Optional[pd.DataFrame] = None
        self.drift_report: Optional[Dict] = None

    def load_all(self):
        """Load all CSV datasets into memory."""
        data_dir = settings.DATA_DIR
        logger.info(f"Loading data from: {data_dir}")

        # ── Transactions ────────────────────────────────────
        path = os.path.join(data_dir, "processed", "clean_retail_data.csv")
        if os.path.exists(path):
            self.df = pd.read_csv(
                path, 
                parse_dates=["InvoiceDate"],
                dtype={
                    "Quantity": "int32",
                    "Price": "float32",
                    "Revenue": "float32",
                    "Customer ID": "int32",
                    "Country": "category",
                    "StockCode": "category",
                    "Description": "category"
                }
            )
            self.df["Year"] = self.df["InvoiceDate"].dt.year.astype("int16")
            self.df["Month"] = self.df["InvoiceDate"].dt.month.astype("int8")
            self.df["Hour"] = self.df["InvoiceDate"].dt.hour.astype("int8")
            self.df["Weekday"] = self.df["InvoiceDate"].dt.day_name().astype("category")
            logger.info(f"  Transactions loaded: {len(self.df):,} rows")
        else:
            logger.warning(f"  Transaction data not found: {path}")

        # ── Segments ────────────────────────────────────────
        path = os.path.join(data_dir, "processed", "customer_segments.csv")
        if os.path.exists(path):
            self.segments = pd.read_csv(path)
            logger.info(f"  Segments loaded: {len(self.segments):,} rows")

        # ── Forecast ────────────────────────────────────────
        path = os.path.join(data_dir, "processed", "sales_forecast.csv")
        if os.path.exists(path):
            self.forecast = pd.read_csv(path, parse_dates=["ds"])
            logger.info(f"  Forecast loaded: {len(self.forecast):,} rows")

        # ── Churn ───────────────────────────────────────────
        path = os.path.join(data_dir, "processed", "churn_data.csv")
        if os.path.exists(path):
            self.churn_df = pd.read_csv(path)
            logger.info(f"  Churn data loaded: {len(self.churn_df):,} rows")

        # ── Drift Report ────────────────────────────────────
        path = os.path.join(data_dir, "processed", "drift_report.json")
        if os.path.exists(path):
            with open(path, "r") as f:
                self.drift_report = json.load(f)
            logger.info("  Drift report loaded")

        logger.info("All data loaded successfully.")

    # ── Filtering ───────────────────────────────────────────
    def get_filtered_df(
        self,
        countries: Optional[List[str]] = None,
        years: Optional[List[int]] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
    ) -> pd.DataFrame:
        """Apply global filters to the transaction dataframe."""
        if self.df is None:
            return pd.DataFrame()
        filtered = self.df.copy()
        if countries:
            filtered = filtered[filtered["Country"].isin(countries)]
        if years:
            filtered = filtered[filtered["Year"].isin(years)]
        if start_date:
            filtered = filtered[filtered["InvoiceDate"].dt.date >= start_date]
        if end_date:
            filtered = filtered[filtered["InvoiceDate"].dt.date <= end_date]
        return filtered

    def get_filtered_segments(self, segments: Optional[List[str]] = None) -> Optional[pd.DataFrame]:
        if self.segments is None:
            return None
        if segments:
            return self.segments[self.segments["Segment"].isin(segments)]
        return self.segments.copy()

    # ── Dashboard KPIs ──────────────────────────────────────
    def get_kpis(self, filtered: pd.DataFrame) -> Dict[str, Any]:
        tot_rev = float(filtered["Revenue"].sum())
        tot_orders = int(filtered["Invoice"].nunique())
        tot_cust = int(filtered["Customer ID"].nunique())
        aov = tot_rev / tot_orders if tot_orders > 0 else 0
        tot_prod = int(filtered["StockCode"].nunique())
        num_countries = int(filtered["Country"].nunique())

        # Sparkline arrays
        monthly_rev = filtered.groupby(["Year", "Month"])["Revenue"].sum().values.tolist()
        monthly_orders = filtered.groupby(["Year", "Month"])["Invoice"].nunique().values.tolist()
        monthly_cust = filtered.groupby(["Year", "Month"])["Customer ID"].nunique().values.tolist()
        monthly_aov = []
        rev_g = filtered.groupby(["Year", "Month"])["Revenue"].sum()
        ord_g = filtered.groupby(["Year", "Month"])["Invoice"].nunique()
        for key in rev_g.index:
            o = ord_g.get(key, 1)
            monthly_aov.append(float(rev_g[key] / o) if o > 0 else 0)

        return {
            "total_revenue": tot_rev,
            "total_orders": tot_orders,
            "total_customers": tot_cust,
            "avg_order_value": float(aov),
            "total_products": tot_prod,
            "num_countries": num_countries,
            "sparklines": {
                "revenue": monthly_rev,
                "orders": monthly_orders,
                "customers": monthly_cust,
                "aov": monthly_aov,
            },
        }

    # ── Monthly Revenue ─────────────────────────────────────
    def get_monthly_revenue(self, filtered: pd.DataFrame) -> List[Dict]:
        monthly = filtered.groupby(["Year", "Month"])["Revenue"].sum().reset_index()
        monthly["Period"] = pd.to_datetime(monthly[["Year", "Month"]].assign(DAY=1))
        return [
            {"period": row["Period"].isoformat(), "revenue": float(row["Revenue"])}
            for _, row in monthly.iterrows()
        ]

    # ── Geographic Revenue ──────────────────────────────────
    def get_geo_revenue(self, filtered: pd.DataFrame) -> List[Dict]:
        geo = filtered.groupby("Country")["Revenue"].sum().reset_index()
        return [
            {"country": row["Country"], "revenue": float(row["Revenue"])}
            for _, row in geo.iterrows()
        ]

    # ── Top Products ────────────────────────────────────────
    def get_top_products(self, filtered: pd.DataFrame, n: int = 10) -> List[Dict]:
        top = filtered.groupby("Description")["Revenue"].sum().sort_values(ascending=False).head(n).reset_index()
        return [
            {"description": row["Description"], "revenue": float(row["Revenue"])}
            for _, row in top.iterrows()
        ]

    # ── Top Countries ───────────────────────────────────────
    def get_top_countries(self, filtered: pd.DataFrame, n: int = 8) -> List[Dict]:
        top = filtered.groupby("Country")["Revenue"].sum().sort_values(ascending=False).head(n).reset_index()
        return [
            {"country": row["Country"], "revenue": float(row["Revenue"])}
            for _, row in top.iterrows()
        ]

    # ── EDA Distributions ───────────────────────────────────
    def get_distributions(self, filtered: pd.DataFrame) -> Dict[str, List[float]]:
        sub_rev = filtered[filtered["Revenue"] < filtered["Revenue"].quantile(0.98)]
        sub_pr = filtered[filtered["Price"] < filtered["Price"].quantile(0.98)]
        sub_qty = filtered[filtered["Quantity"] < filtered["Quantity"].quantile(0.98)]
        return {
            "revenue": sub_rev["Revenue"].tolist(),
            "price": sub_pr["Price"].tolist(),
            "quantity": sub_qty["Quantity"].tolist(),
        }

    # ── Temporal Heatmap ────────────────────────────────────
    def get_temporal_heatmap(self, filtered: pd.DataFrame) -> Dict:
        weekday_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        pivot = filtered.pivot_table(index="Weekday", columns="Hour", values="Revenue", aggfunc="sum")
        pivot = pivot.reindex(weekday_order)
        return {
            "weekdays": weekday_order,
            "hours": list(range(24)),
            "values": pivot.where(pivot.notna(), None).values.tolist(),
        }

    # ── Weekly Revenue ──────────────────────────────────────
    def get_weekly_revenue(self, filtered: pd.DataFrame) -> List[Dict]:
        weekday_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        weekly = filtered.groupby("Weekday")["Revenue"].sum().reindex(weekday_order).reset_index()
        return [
            {"weekday": row["Weekday"], "revenue": float(row["Revenue"])}
            for _, row in weekly.iterrows()
        ]

    # ── Correlations ────────────────────────────────────────
    def get_correlations(self, filtered: pd.DataFrame) -> Dict:
        cols = ["Quantity", "Price", "Revenue"]
        corr = filtered[cols].corr()
        return {
            "labels": cols,
            "matrix": corr.values.tolist(),
        }

    # ── Stats ───────────────────────────────────────────────
    def get_stats(self, filtered: pd.DataFrame) -> List[Dict]:
        desc = filtered[["Quantity", "Price", "Revenue"]].describe().T
        rows = []
        for metric in desc.index:
            rows.append({
                "metric": metric,
                **{col: float(desc.loc[metric, col]) for col in desc.columns},
            })
        return rows

    # ── Treemap Data ────────────────────────────────────────
    def get_treemap_data(self, filtered: pd.DataFrame, n: int = 35) -> List[Dict]:
        top = filtered.groupby("Description")["Revenue"].sum().sort_values(ascending=False).head(n).reset_index()
        return [
            {"description": row["Description"], "revenue": float(row["Revenue"])}
            for _, row in top.iterrows()
        ]

    # ── Scatter Data ────────────────────────────────────────
    def get_scatter_data(self, filtered: pd.DataFrame, n: int = 1500) -> List[Dict]:
        sample = filtered.sample(min(len(filtered), n), random_state=42)
        return [
            {"quantity": float(r["Quantity"]), "price": float(r["Price"]), "revenue": float(r["Revenue"])}
            for _, r in sample.iterrows()
        ]

    # ── Segment Composition ─────────────────────────────────
    def get_segment_composition(self, segs: pd.DataFrame) -> List[Dict]:
        counts = segs["Segment"].value_counts().reset_index()
        counts.columns = ["segment", "count"]
        return counts.to_dict(orient="records")

    # ── Segment Profile ─────────────────────────────────────
    def get_segment_profile(self, segs: pd.DataFrame) -> List[Dict]:
        profile = segs.groupby("Segment")[["Recency", "Frequency", "Monetary"]].mean().round(1).reset_index()
        return [
            {"segment": r["Segment"], "recency": r["Recency"], "frequency": r["Frequency"], "monetary": r["Monetary"]}
            for _, r in profile.iterrows()
        ]

    # ── 3D Cluster Points ───────────────────────────────────
    def get_cluster_3d(self, segs: pd.DataFrame, n: int = 1800) -> List[Dict]:
        sample = segs.sample(min(len(segs), n), random_state=42)
        return [
            {"recency": int(r["Recency"]), "frequency": int(r["Frequency"]),
             "monetary": float(r["Monetary"]), "segment": r["Segment"]}
            for _, r in sample.iterrows()
        ]

    # ── Forecast Data ───────────────────────────────────────
    def get_forecast_data(self, horizon_days: int = 90) -> Dict:
        if self.forecast is None:
            return {"points": [], "summary": None, "actual_daily": []}

        fore = self.forecast.head(len(self.forecast) - max(0, 90 - horizon_days))
        max_date = self.df["InvoiceDate"].max() if self.df is not None else pd.Timestamp.min

        future_fore = fore[fore["ds"] > max_date]
        proj_total = float(future_fore["yhat"].sum()) if len(future_fore) > 0 else 0
        proj_avg = float(future_fore["yhat"].mean()) if len(future_fore) > 0 else 0

        # Actual daily sales for overlay
        actual_daily = []
        if self.df is not None:
            daily = self.df.groupby(self.df["InvoiceDate"].dt.date)["Revenue"].sum().reset_index()
            actual_daily = [
                {"ds": str(r["InvoiceDate"]), "revenue": float(r["Revenue"])}
                for _, r in daily.iterrows()
            ]

        points = [
            {"ds": r["ds"].isoformat() if hasattr(r["ds"], "isoformat") else str(r["ds"]),
             "yhat": round(float(r["yhat"]), 2),
             "yhat_lower": round(float(r["yhat_lower"]), 2),
             "yhat_upper": round(float(r["yhat_upper"]), 2)}
            for _, r in fore.iterrows()
        ]

        # Future-only table
        table = [
            {"ds": r["ds"].isoformat() if hasattr(r["ds"], "isoformat") else str(r["ds"]),
             "yhat": round(float(r["yhat"]), 2),
             "yhat_lower": round(float(r["yhat_lower"]), 2),
             "yhat_upper": round(float(r["yhat_upper"]), 2)}
            for _, r in future_fore.iterrows()
        ]

        return {
            "points": points,
            "table": table,
            "actual_daily": actual_daily,
            "summary": {"projected_total": proj_total, "projected_avg_daily": proj_avg, "horizon_days": horizon_days},
        }

    # ── Churn Overview ──────────────────────────────────────
    def get_churn_overview(self) -> Optional[Dict]:
        if self.churn_df is None:
            return None
        total = len(self.churn_df)
        churned = int(self.churn_df["Churn"].sum())
        return {
            "total_customers": total,
            "churned_customers": churned,
            "churn_rate": float(churned / total) if total > 0 else 0,
        }

    # ── Churn Risk List ─────────────────────────────────────
    def get_churn_risk_list(self, n: int = 100) -> List[Dict]:
        if self.churn_df is None:
            return []
        risk = self.churn_df[self.churn_df["Churn"] == 1].sort_values("Recency", ascending=False).head(n)
        return [
            {"customer_id": int(r["Customer ID"]), "recency": int(r["Recency"]),
             "frequency": int(r["Frequency"]), "monetary": float(r["Monetary"])}
            for _, r in risk.iterrows()
        ]

    # ── Inventory Health ────────────────────────────────────
    def calculate_inventory_metrics(self) -> pd.DataFrame:
        """Port of the Streamlit inventory health calculator."""
        if self.df is None:
            return pd.DataFrame()

        daily_sales = self.df.groupby(
            ["Description", self.df["InvoiceDate"].dt.date]
        )["Quantity"].sum().reset_index()
        product_stats = daily_sales.groupby("Description").agg(
            avg_daily_sales=("Quantity", "mean"),
            max_daily_sales=("Quantity", "max"),
            total_sold=("Quantity", "sum"),
        ).reset_index()

        lead_time = 7
        product_stats["safety_stock"] = (
            (product_stats["max_daily_sales"] - product_stats["avg_daily_sales"]) * lead_time
        ).round(0).astype(int).clip(lower=0)

        product_stats["reorder_point"] = (
            (product_stats["avg_daily_sales"] * lead_time) + product_stats["safety_stock"]
        ).round(0).astype(int).clip(lower=0)

        np.random.seed(42)
        multipliers = np.random.choice(
            [0.3, 0.7, 1.2, 1.8], size=len(product_stats), p=[0.05, 0.12, 0.53, 0.30]
        )
        product_stats["current_stock"] = (
            product_stats["reorder_point"] * multipliers
        ).round(0).astype(int).clip(lower=0)

        def get_status(row):
            if row["current_stock"] <= row["safety_stock"]:
                return "Critical Low Stock"
            elif row["current_stock"] <= row["reorder_point"]:
                return "Reorder Alert"
            else:
                return "Healthy Stock"

        product_stats["status"] = product_stats.apply(get_status, axis=1)
        return product_stats

    def get_inventory_summary(self, inv: pd.DataFrame) -> Dict:
        return {
            "total_skus": len(inv),
            "critical_skus": len(inv[inv["status"] == "Critical Low Stock"]),
            "reorder_skus": len(inv[inv["status"] == "Reorder Alert"]),
            "healthy_skus": len(inv[inv["status"] == "Healthy Stock"]),
        }

    def get_inventory_items(self, inv: pd.DataFrame, status_filter: Optional[str] = None) -> List[Dict]:
        if status_filter and status_filter != "all":
            inv = inv[inv["status"] == status_filter]
        return [
            {
                "description": r["Description"],
                "avg_daily_sales": round(float(r["avg_daily_sales"]), 2),
                "safety_stock": int(r["safety_stock"]),
                "reorder_point": int(r["reorder_point"]),
                "current_stock": int(r["current_stock"]),
                "status": r["status"],
            }
            for _, r in inv.iterrows()
        ]

    # ── Available Filters ───────────────────────────────────
    def get_available_filters(self) -> Dict:
        if self.df is None:
            return {}
        return {
            "countries": sorted(self.df["Country"].unique().tolist()),
            "years": sorted(self.df["Year"].unique().tolist()),
            "min_date": str(self.df["InvoiceDate"].min().date()),
            "max_date": str(self.df["InvoiceDate"].max().date()),
            "segments": ["Premium Customers", "Loyal Customers", "Regular Customers", "At Risk Customers"],
        }


# Singleton instance
data_service = DataService()
