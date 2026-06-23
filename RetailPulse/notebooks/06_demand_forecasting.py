# ============================================================
# RetailPulse - Phase 7: Demand Forecasting (Prophet)
# Notebook: 06_demand_forecasting.ipynb
# ============================================================

import pandas as pd
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

plt.rcParams['figure.figsize'] = (14, 6)
IMAGES_PATH = "../images/"

# ── Step 1: Load Data & Prepare Daily Sales ──────────────────
"""
PROPHET INPUT:
- Prophet expects 2 columns: 'ds' (date) and 'y' (value)
- Daily revenue aggregate karto
"""
df = pd.read_csv("../data/processed/clean_retail_data.csv", parse_dates=['InvoiceDate'])
df['Revenue'] = df['Quantity'] * df['Price']

daily_sales = df.groupby(df['InvoiceDate'].dt.date)['Revenue'].sum().reset_index()
daily_sales.columns = ['ds', 'y']
daily_sales['ds'] = pd.to_datetime(daily_sales['ds'])

print(f"✅ Daily Sales prepared: {len(daily_sales)} days")
print(daily_sales.tail())


# ── Step 2: Train Prophet Model ──────────────────────────────
"""
PROPHET:
- Facebook (Meta) ne banawlela forecasting library
- Seasonality (weekly, yearly) automatically detect karto
- Missing values handle karto
- Holidays handle karto
"""
try:
    from prophet import Prophet

    model = Prophet(
        yearly_seasonality=True,    # Annual patterns capture karto
        weekly_seasonality=True,    # Weekly patterns capture karto
        daily_seasonality=False,    # Daily too granular - off rakhtoy
        changepoint_prior_scale=0.05  # Trend flexibility
    )

    model.fit(daily_sales)
    print("✅ Prophet model trained!")

    # ── Step 3: Forecast Next 90 Days ───────────────────────
    future = model.make_future_dataframe(periods=90)
    forecast = model.predict(future)

    # ── Step 4: Visualize Forecast ───────────────────────────
    plt.figure(figsize=(14, 6))
    model.plot(forecast, ax=plt.gca())
    plt.title("Sales Forecast – Next 90 Days", fontweight='bold')
    plt.xlabel("Date")
    plt.ylabel("Revenue (£)")
    plt.tight_layout()
    plt.savefig(f"{IMAGES_PATH}13_forecast.png", dpi=150)
    plt.show()

    # ── Step 5: Seasonality Components ──────────────────────
    fig2 = model.plot_components(forecast)
    plt.tight_layout()
    plt.savefig(f"{IMAGES_PATH}14_seasonality.png", dpi=150)
    plt.show()
    print("📌 Insight: November-December madhe peak sales expected - holiday demand")

    # Save forecast
    forecast[['ds','yhat','yhat_lower','yhat_upper']].to_csv(
        "../data/processed/sales_forecast.csv", index=False)
    print("✅ Saved: sales_forecast.csv")

except ImportError:
    print("⚠️  Prophet not installed. Run: pip install prophet")
    print("   Alternative: ARIMA use karo (see below)")

    # ARIMA Alternative
    print("\n--- ARIMA Alternative ---")
    print("from statsmodels.tsa.arima.model import ARIMA")
    print("model = ARIMA(daily_sales['y'], order=(5,1,0))")
    print("model_fit = model.fit()")
    print("forecast = model_fit.forecast(steps=90)")

print("\n✅ Phase 7 - Forecasting Complete!")
print("➡️  Next: Open 07_churn_prediction.ipynb")
