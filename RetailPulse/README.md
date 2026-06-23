# 🛒 RetailPulse – AI-Powered Customer Analytics & Demand Forecasting

![Python](https://img.shields.io/badge/Python-3.9+-blue)
![Status](https://img.shields.io/badge/Status-In%20Progress-yellow)

---

## 📌 Project Overview

**RetailPulse** is a complete end-to-end Data Science & Machine Learning project built during a Data Science & Analytics Internship.

It uses the **Online Retail II Dataset (2009–2011)** to perform:
- 📊 Exploratory Data Analysis (EDA)
- 👥 Customer Segmentation using RFM + KMeans
- 📈 Demand Forecasting using Prophet
- ⚠️ Customer Churn Prediction using ML models
- 🖥️ Interactive Streamlit Dashboard

---

## 🛠️ Technologies Used

| Category        | Tools/Libraries                        |
|----------------|----------------------------------------|
| Language        | Python 3.9+                            |
| Data Handling   | Pandas, NumPy                          |
| Visualization   | Matplotlib, Seaborn, Plotly            |
| ML Models       | Scikit-Learn, XGBoost                  |
| Forecasting     | Prophet                                |
| Dashboard       | Streamlit                              |
| Notebook        | JupyterLab                             |

---

## 📁 Folder Structure

```
RetailPulse/
│
├── data/
│   ├── raw/              ← Original dataset (never edit this)
│   └── processed/        ← Cleaned data saved here
│
├── notebooks/            ← All Jupyter Notebooks (EDA, Models, etc.)
├── models/               ← Saved ML models (.pkl files)
├── dashboard/            ← Streamlit dashboard app
├── reports/              ← Final project report (PDF)
├── presentation/         ← PowerPoint slides
├── images/               ← All charts and graphs
└── app/                  ← Additional web app files
```

---

## 📊 Dataset

- **Name:** Online Retail II Dataset
- **Source:** UCI Machine Learning Repository
- **Period:** 2009–2011
- **Size:** ~1 Million+ rows (after merging both sheets)

### Columns:
| Column       | Description                        |
|-------------|-------------------------------------|
| Invoice      | Invoice number                      |
| StockCode    | Product code                        |
| Description  | Product name                        |
| Quantity     | Number of units sold                |
| InvoiceDate  | Date and time of purchase           |
| Price        | Unit price                          |
| Customer ID  | Unique customer identifier          |
| Country      | Country of customer                 |

---

## 🚀 How to Run

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/RetailPulse.git
cd RetailPulse
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Add Dataset
Place `online_retail_II.xlsx` inside `data/raw/` folder.

### 4. Run Notebooks
```bash
jupyter lab
```
Open notebooks in order:
- `01_data_loading.ipynb`
- `02_data_cleaning.ipynb`
- `03_eda.ipynb`
- `04_feature_engineering.ipynb`
- `05_customer_segmentation.ipynb`
- `06_demand_forecasting.ipynb`
- `07_churn_prediction.ipynb`

### 5. Launch Dashboard
```bash
streamlit run dashboard/app.py
```

---

## 📈 Project Phases

| Phase | Description                   | Status |
|-------|-------------------------------|--------|
| 1     | Project Setup                 | ✅ Done |
| 2     | Data Loading                  | ⬜ Pending |
| 3     | Data Cleaning                 | ⬜ Pending |
| 4     | EDA                           | ⬜ Pending |
| 5     | Feature Engineering           | ⬜ Pending |
| 6     | Customer Segmentation         | ⬜ Pending |
| 7     | Demand Forecasting            | ⬜ Pending |
| 8     | Churn Prediction              | ⬜ Pending |
| 9     | Streamlit Dashboard           | ⬜ Pending |

---

## 👨‍💻 Author

**[Your Name]**
Data Science & Analytics Intern

---

## 📄 License

This project is for educational/internship purposes.
