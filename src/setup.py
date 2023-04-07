
from models.status import Status
from models.temperature_requirements import TemperatureRequirements
from db import SessionLocal, engine, Base

def create_app():
    db_session = SessionLocal() 
    Base.metadata.create_all(bind=engine)
    TemperatureRequirements.populate_default_requirements(db_session)
    Status.populate_first_entry(db_session)
    db_session.close()

if __name__ == "__main__":
    create_app()