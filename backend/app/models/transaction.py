from sqlalchemy import Column, Integer, String, Float, DateTime, BigInteger
from app.database import Base


class Transaction(Base):
    """Retail transaction record (maps to clean_retail_data.csv)."""
    __tablename__ = "transactions"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    invoice = Column(Integer, nullable=False, index=True)
    stock_code = Column(String(50), nullable=False)
    description = Column(String(500), nullable=True)
    quantity = Column(Integer, nullable=False)
    invoice_date = Column(DateTime, nullable=False, index=True)
    price = Column(Float, nullable=False)
    customer_id = Column(Integer, nullable=False, index=True)
    country = Column(String(100), nullable=False, index=True)
    revenue = Column(Float, nullable=False)
