"""
Database models
"""

from sqlalchemy import Column, Integer, String, Float, BigInteger, Text, TIMESTAMP
from sqlalchemy.sql import func
from app.database import Base


class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(BigInteger, nullable=False)
    model_name = Column(String(50))
    model_version = Column(String(20))
    text_length = Column(Integer)
    prediction = Column(Integer)  # 0 = valid, 1 = hoax
    prob_hoax = Column(Float)
    confidence = Column(Float)
    user_label = Column(Integer)  # 0 = valid, 1 = hoax
    agreement = Column(String(20))
    raw_text = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())

    def to_dict(self):
        """Convert to dictionary"""
        return {
            "id": self.id,
            "timestamp": self.timestamp,
            "model_name": self.model_name,
            "model_version": self.model_version,
            "text_length": self.text_length,
            "prediction": self.prediction,
            "prob_hoax": self.prob_hoax,
            "confidence": self.confidence,
            "user_label": self.user_label,
            "agreement": self.agreement,
            "raw_text": self.raw_text,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
