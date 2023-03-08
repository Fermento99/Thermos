from db.db import db
import datetime


class History(db.Model):
    time = db.Column(db.DateTime, primary_key=True)
    salon = db.Column(db.Float)
    bedroom = db.Column(db.Float)
    bathroom = db.Column(db.Float)
    pawel = db.Column(db.Float)
    michal = db.Column(db.Float)

    def __init__(self, **kwargs) -> None:
        if 'time' in kwargs:
            kwargs['time'] = datetime.datetime.fromisoformat(kwargs['time'])
        else:
            kwargs['time'] = datetime.datetime.now()

        super().__init__(**kwargs)

    def to_dict(self) -> dict:
        return {
            'time': self.time,
            'salon': self.salon,
            'bedroom': self.bedroom,
            'bathroom': self.bathroom,
            'pawel': self.pawel,
            'michal': self.michal,
        }