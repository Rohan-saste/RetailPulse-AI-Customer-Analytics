from sqlalchemy import Column, Integer, String, Float
from app.database import Base


class CustomerSegment(Base):
    """Customer segmentation record (maps to customer_segments.csv)."""
    __tablename__ = "customer_segments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, nullable=False, unique=True, index=True)
    recency = Column(Integer, nullable=False)
    frequency = Column(Integer, nullable=False)
    monetary = Column(Float, nullable=False)
    cluster = Column(Integer, nullable=False)
    segment = Column(String(100), nullable=False, index=True)
