from db import Base
from sqlalchemy import Column, Float, DateTime, select
import datetime


class TemperatureStatus(Base):
    __tablename__ = 'temperature_status'

    time = Column(DateTime, primary_key=True)
    livingroom = Column(Float, nullable=False)
    bedroom = Column(Float, nullable=False)
    bathroom = Column(Float, nullable=False)
    pawel = Column(Float, nullable=False)
    michal = Column(Float, nullable=False)

    def __init__(self, **kwargs) -> None:
        if 'time' in kwargs:
            kwargs['time'] = datetime.datetime.fromisoformat(kwargs['time'])
        else:
            kwargs['time'] = datetime.datetime.now()

        super().__init__(**kwargs)
    
    @staticmethod
    def get_now(session):
        result = session.execute(
            select(TemperatureStatus.__table__.columns)
                .order_by(TemperatureStatus.time.desc())
                .limit(1)
            ).fetchall()
        return [dict(row._mapping) for row in result]
    
    @staticmethod
    def get_history(session, room, limit):
        offset = datetime.datetime.now() - datetime.timedelta(hours=limit)
        if room in TemperatureStatus.__table__.columns.keys():
            result = session.execute(
                select(TemperatureStatus.time, TemperatureStatus.__table__.columns[room])
                    .where(TemperatureStatus.time > offset)
                    .order_by(TemperatureStatus.time.desc())
                ).fetchall()
            return [dict(row._mapping) for row in result]
        raise NameError('room name doesn\'t exist in the database')