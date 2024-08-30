from sqlalchemy import Column, Integer, Float, String, Enum, DateTime, func
from sqlalchemy.orm import relationship
from ..db import db

class TransactionModel(db.Model):
    __tablename__ = "transaction"
    id = Column(Integer, primary_key=True)
    amount = Column(Float, nullable=False)
    description = Column(String(255), nullable=True)
    category_id = Column(Integer, db.ForeignKey('category.id'), nullable=True)  
    category = relationship("Category", back_populates="transactions")
    type = Column(Enum("expense", "income", name="transaction_types"), nullable=False)
    user_id = Column(Integer, db.ForeignKey("user.id"), nullable=False)
    user = relationship("UserModel", back_populates="transactions", lazy=True)
    date_created = Column(DateTime, default=func.now(), nullable=False)

    def __init__(self, amount, description, category_id, type, user_id, date_created):
        self.amount = amount
        self.description = description
        self.category_id = category_id
        self.type = type  
        self.user_id = user_id
        self.date_created = date_created
