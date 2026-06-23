from sqlalchemy import Column, Integer, String, DateTime, func
from app.database import Base


class User(Base):
    """Application user for JWT authentication."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=True)
    role = Column(String(50), nullable=False, default="analyst")  # admin | analyst
    created_at = Column(DateTime, server_default=func.now())
