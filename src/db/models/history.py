from db.db import db
import datetime


class History(db.Model):
    time = db.Column(db.DateTime, primary_key=True)
    salon = db.Column(db.Float, nullable=False)
    bedroom = db.Column(db.Float, nullable=False)
    bathroom = db.Column(db.Float, nullable=False)
    pawel = db.Column(db.Float, nullable=False)
    michal = db.Column(db.Float, nullable=False)

    def __init__(self, **kwargs) -> None:
        if 'time' in kwargs:
            kwargs['time'] = datetime.datetime.fromisoformat(kwargs['time'])
        else:
            kwargs['time'] = datetime.datetime.now()

        super().__init__(**kwargs)
    
    @staticmethod
    def get_now():
        result = db.session.execute(
            db.select(History.__table__.columns)
                .order_by(History.time.desc())
                .limit(1)
            ).fetchall()
        return [dict(row._mapping) for row in result]
    
    @staticmethod
    def get_history(room, limit):
        offset = datetime.datetime.now() - datetime.timedelta(hours=limit)
        if room in History.__table__.columns.keys():
            result = db.session.execute(
                db.select(History.time, History.__table__.columns[room])
                    .where(History.time > offset)
                    .order_by(History.time.desc())
                ).fetchall()
            return [dict(row._mapping) for row in result]
        raise NameError('room name doesn\'t exist in the database')