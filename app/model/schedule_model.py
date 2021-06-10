import datetime

from sqlalchemy import ForeignKey

from app import db


class Schedule(db.Model):
    __tablename__ = 'schedule'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    day = db.Column(db.Integer, nullable=True)  # 2-8
    start_time = db.Column(db.String, nullable=True)
    end_time = db.Column(db.String, nullable=True)

    post_id = db.Column(db.Integer, ForeignKey('post.id'))

    created_date = db.Column(db.DateTime, nullable=True)
    updated_date = db.Column(db.DateTime, nullable=True)

    def __init__(self, day, start_time, end_time, post_id):
        self.day = day
        self.start_time = start_time
        self.end_time = end_time
        self.post_id = post_id
        self.created_date = datetime.datetime.now()
        self.updated_date = datetime.datetime.now()

    def to_json(self):
        return {
            'id': self.id,
            'day': self.day,
            'start_time': self.start_time,
            'end_time': self.end_time
        }

    @staticmethod
    def to_json_list(schedules):
        schedules = sorted(schedules, key=lambda x: x.day)
        return [schedule.to_json() for schedule in schedules]
