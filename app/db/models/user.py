from sqlalchemy import CheckConstraint, Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.models.base import TimedBaseModel


class User(TimedBaseModel):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(64), unique=True, index=True)
    email = Column(String(128), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    
    receipts = relationship("Receipt", back_populates="user", cascade="all, delete-orphan")
    
    __table_args__ = (
        CheckConstraint("length(username) >= 3", name='check_username_length'),
        CheckConstraint("length(email) >= 5", name='check_email_length')
    )
    
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"
