from db import Base
from sqlalchemy import Column, Boolean, DateTime, select
from datetime import datetime, timedelta

class HeatingStatus(Base):
    __tablename__ = 'heating_status'

    time = Column(DateTime, primary_key=True)
    heating = Column(Boolean, nullable=False)
    livingroom = Column(Boolean, nullable=False)
    bedroom = Column(Boolean, nullable=False)
    bathroom = Column(Boolean, nullable=False)
    pawel = Column(Boolean, nullable=False)
    michal = Column(Boolean, nullable=False)

    @staticmethod
    def get_last_entry(session):
        result = session.execute(
            select(HeatingStatus.__table__.columns)
            .order_by(HeatingStatus.time.desc())
            .limit(1)
        ).fetchall()
        return [dict(row._mapping) for row in result][0]
    
    @staticmethod
    def get_history(session, room, limit):
        offset = datetime.now() - timedelta(hours=limit)
        if room in HeatingStatus.__table__.columns.keys():
            result = session.execute(
                select(HeatingStatus.time, HeatingStatus.__table__.columns[room])
                    .where(HeatingStatus.time > offset)
                    .order_by(HeatingStatus.time.desc())
                ).fetchall()
            return [dict(row._mapping) for row in result]
        raise NameError('room name doesn\'t exist in the database')
    
    @staticmethod
    def populate_first_entry(session):
        now = datetime.now()
        first_heating_status = {
            'time': now,
            'heating': False,
            'livingroom': False,
            'bedroom': False,
            'bathroom': False,
            'pawel': False,
            'michal': False,
        }
        session.add(HeatingStatus(**first_heating_status))
        session.commit()
