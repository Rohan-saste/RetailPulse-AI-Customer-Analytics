from sqlalchemy import Column, Integer, Float
from app.database import Base


class ChurnRecord(Base):
    """Customer churn risk record (maps to churn_data.csv)."""
    __tablename__ = "churn_records"

    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, nullable=False, unique=True, index=True)
    recency = Column(Integer, nullable=False)
    frequency = Column(Integer, nullable=False)
    monetary = Column(Float, nullable=False)
    avg_revenue = Column(Float, nullable=False)
    total_items = Column(Integer, nullable=False)
    avg_quantity = Column(Float, nullable=False)
    churn = Column(Integer, nullable=False)  # 0 or 1
