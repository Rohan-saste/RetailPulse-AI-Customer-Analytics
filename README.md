# RetailPulse – Enterprise BI Dashboard

RetailPulse is a production-ready full-stack web application providing executive analytics, customer segmentation, demand forecasting, and inventory health tracking.

## Architecture

* **Backend**: FastAPI (Python)
* **Frontend**: React + Vite + Tailwind CSS
* **Database**: SQLite (via SQLAlchemy)
* **Machine Learning**: Scikit-learn (Churn prediction), custom algorithms (Inventory & Segmentation)

## Quick Start

### 1. Backend Setup

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env

# Start FastAPI server
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`. Swagger documentation is available at `http://localhost:8000/docs`.

### 2. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

The web app will be available at `http://localhost:5173`.

## Deployment

* **Frontend**: Deploys automatically to Vercel via the `vercel.json` config.
* **Backend**: Deploys automatically to Render via the `render.yaml` config.

Ensure environment variables defined in `.env.example` are securely set in your deployment environments.
# RetailPulse-AI-Customer-Analytics
# RetailPulse-AI-Customer-Analytics
