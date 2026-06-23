from sqlalchemy import Column, Integer, Float, DateTime
from app.database import Base


class Forecast(Base):
    """Sales forecast record (maps to sales_forecast.csv)."""
    __tablename__ = "forecasts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    ds = Column(DateTime, nullable=False, index=True)
    yhat = Column(Float, nullable=False)
    yhat_lower = Column(Float, nullable=False)
    yhat_upper = Column(Float, nullable=False)
