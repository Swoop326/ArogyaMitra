from sqlalchemy import Column, Integer, Float, ForeignKey
from config.database import Base

class Progress(Base):
    __tablename__ = "progress"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    weight = Column(Float)
    body_fat = Column(Float)