from sqlalchemy import Column, Integer, Float, DateTime
from config.database import Base
from datetime import datetime


class BodyMetrics(Base):

    __tablename__ = "body_metrics"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer)

    height = Column(Float)
    weight = Column(Float)

    bmi = Column(Float)

    body_fat_percent = Column(Float)

    muscle_mass = Column(Float)

    created_at = Column(DateTime, default=datetime.utcnow)
