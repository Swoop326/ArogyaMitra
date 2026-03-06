from sqlalchemy import Column, Integer, String, ForeignKey
from config.database import Base

class HealthAssessment(Base):
    __tablename__ = "health_assessments"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    condition = Column(String)