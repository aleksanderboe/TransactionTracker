from ..db import db
from werkzeug.security import check_password_hash
from sqlalchemy.orm import relationship

class UserModel(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    profile_picture = db.Column(db.String(255), nullable=True) 
    transactions = relationship("TransactionModel", back_populates="user", lazy=True, cascade="all, delete-orphan")
    categories = relationship("Category", back_populates="user", lazy=True, cascade="all, delete-orphan")
    
    def __init__(self, username, password_hash, profile_picture=""):
        self.username = username
        self.password_hash = password_hash
        self.profile_picture = profile_picture
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
