from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from ..db import db

class Category(db.Model):
    __tablename__ = "category"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    color = Column(String(7), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)

    user = relationship("UserModel", back_populates="categories")
    transactions = relationship("TransactionModel", back_populates="category")
