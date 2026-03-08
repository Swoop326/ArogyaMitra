from sqlalchemy import Column, Integer, String
from config.database import Base


class HealthProfile(Base):

    __tablename__ = "health_profiles"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer)

    heart_conditions = Column(String)
    diabetes = Column(String)
    blood_pressure = Column(String)

    knee_injury = Column(String)
    back_pain = Column(String)
    other_injuries = Column(String)

    food_allergies = Column(String)
    medication_allergies = Column(String)

    current_medication = Column(String)
    supplements = Column(String)

    fitness_goal = Column(String)
