from db import Base
from sqlalchemy import Column, Float, Boolean, DateTime, select
from datetime import datetime, timedelta


class Status(Base):
    __tablename__ = 'status'

    time = Column(DateTime, primary_key=True)
    heating = Column(Boolean)
    livingroom_temperature = Column(Float)
    bedroom_temperature = Column(Float)
    bathroom_temperature = Column(Float)
    pawel_temperature = Column(Float)
    michal_temperature = Column(Float)
    livingroom_heating = Column(Boolean)
    bedroom_heating = Column(Boolean)
    bathroom_heating = Column(Boolean)
    pawel_heating = Column(Boolean)
    michal_heating = Column(Boolean)

    rooms = [
        'livingroom',
        'bedroom',
        'bathroom',
        'pawel',
        'michal'
    ]

    @staticmethod
    def get_last_entry(session):
        result = session.execute(
            select(Status.__table__.columns)
                .order_by(Status.time.desc())
                .limit(1)
            ).fetchall()
        return [dict(row._mapping) for row in result][0]
    
    @staticmethod
    def get_history(session, room, limit):
        offset = datetime.now() - timedelta(hours=limit)
        if room in Status.rooms:
            temperature_column = '{room}_temperature'.format(room=room)
            heating_column = '{room}_heating'.format(room=room)

            result = session.execute(
                select(
                    Status.time, 
                    Status.__table__.columns[temperature_column].label('temperature'),
                    Status.__table__.columns[heating_column].label('heating'),
                )
                .where(Status.time > offset)
                .order_by(Status.time.desc())
            ).fetchall()
            return [dict(row._mapping) for row in result]
        raise NameError('room name doesn\'t exist in the database')
    
    @staticmethod
    def populate_first_entry(session):
        first_heating_status = {
            'time': datetime.fromtimestamp(0),
            'heating': False,
            'livingroom_temperature': 0,
            'bedroom_temperature': 0,
            'bathroom_temperature': 0,
            'pawel_temperature': 0,
            'michal_temperature': 0,
            'livingroom_heating': False,
            'bedroom_heating': False,
            'bathroom_heating': False,
            'pawel_heating': False,
            'michal_heating': False,
        }
        session.add(Status(**first_heating_status))
        session.commit()