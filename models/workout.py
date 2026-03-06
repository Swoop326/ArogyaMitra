from sqlalchemy import Column, Integer, String, ForeignKey
from config.database import Base

class WorkoutPlan(Base):
    __tablename__ = "workout_plans"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    goal = Column(String)
    duration = Column(String)