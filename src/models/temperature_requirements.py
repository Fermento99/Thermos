from db import Base
from sqlalchemy import Column, Float, Integer, select


class TemperatureRequirements(Base):
    __tablename__ = 'temperature_requirements'

    weekday = Column(Integer, primary_key=True)
    hour = Column(Integer, primary_key=True)
    livingroom = Column(Float, nullable=False)
    bedroom = Column(Float, nullable=False)
    bathroom = Column(Float, nullable=False)
    pawel = Column(Float, nullable=False)
    michal = Column(Float, nullable=False)

    @staticmethod
    def populate_default_requirements(session): 
        for weekday in range(7):
            if weekday in range(5):                    
                entries = [
                    {
                        'hour': 0,
                        'bathroom': 19,
                        'michal': 19,
                        'pawel': 19,
                        'livingroom': 19,
                        'bedroom': 19,
                    },
                    {
                        'hour': 15,
                        'bathroom': 19,
                        'michal': 21.5,
                        'pawel': 20.5,
                        'livingroom': 22,
                        'bedroom': 19,
                    },
                    {
                        'hour': 22,
                        'bathroom': 19,
                        'michal': 19,
                        'pawel': 19,
                        'livingroom': 19,
                        'bedroom': 19,
                    },
                ] 
            else:
                entries = [
                    {
                        'hour': 0,
                        'bathroom': 19,
                        'michal': 19,
                        'pawel': 19,
                        'livingroom': 19,
                        'bedroom': 19,
                    },
                    {
                        'hour': 8,
                        'bathroom': 20,
                        'michal': 19,
                        'pawel': 19,
                        'livingroom': 19,
                        'bedroom': 19,
                    },
                    {
                        'hour': 9,
                        'bathroom': 20.5,
                        'michal': 20.5,
                        'pawel': 20.5,
                        'livingroom': 19,
                        'bedroom': 19,
                    },
                    {
                        'hour': 10,
                        'bathroom': 20.5,
                        'michal': 21,
                        'pawel': 20.5,
                        'livingroom': 22,
                        'bedroom': 19,
                    },
                    {
                        'hour': 15,
                        'bathroom': 20.5,
                        'michal': 21.5,
                        'pawel': 20.5,
                        'livingroom': 22,
                        'bedroom': 19,
                    },
                    {
                        'hour': 20,
                        'bathroom': 21,
                        'michal': 21.5,
                        'pawel': 20.5,
                        'livingroom': 22,
                        'bedroom': 19,
                    },
                    {
                        'hour': 22,
                        'bathroom': 19,
                        'michal': 19,
                        'pawel': 19,
                        'livingroom': 19,
                        'bedroom': 19,
                    },
                ]
            
            for entry in entries:
                entry['weekday'] = weekday
                session.add(TemperatureRequirements(**entry))
            
            session.commit()
    
    @staticmethod
    def get_current_requirements(session, weekday, hour):
        result = session.execute(
            select(TemperatureRequirements.__table__.columns)
            .where(
                (TemperatureRequirements.weekday == weekday) & 
                (TemperatureRequirements.hour <= hour)
            ).order_by(TemperatureRequirements.hour.desc())
            .limit(1)
        ).fetchall()
        return [dict(row._mapping) for row in result][0]
