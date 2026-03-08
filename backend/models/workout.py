from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from config.database import Base



class WorkoutPlan(Base):
    __tablename__ = "workout_plans"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    goal = Column(String)
    level = Column(String)
    days = Column(Integer)

    # store the AI plan JSON as text
    plan_json = Column(Text)

    # progress tracking
    current_day = Column(Integer, default=1)