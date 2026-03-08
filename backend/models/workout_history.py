from sqlalchemy import Column, Integer, DateTime, ForeignKey
from datetime import datetime
from config.database import Base


class WorkoutHistory(Base):

    __tablename__ = "workout_history"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, index=True)

    workout_id = Column(Integer, ForeignKey("workout_plans.id"))

    day = Column(Integer)

    calories = Column(Integer)

    completed_at = Column(DateTime, default=datetime.utcnow)
