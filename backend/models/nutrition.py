from sqlalchemy import Column, Integer, String, ForeignKey
from config.database import Base


class NutritionPlan(Base):
    __tablename__ = "nutrition_plans"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    diet_type = Column(String)
    calories = Column(Integer)
