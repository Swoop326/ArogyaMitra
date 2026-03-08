from config.database import engine, Base
import models  # loads all models

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)