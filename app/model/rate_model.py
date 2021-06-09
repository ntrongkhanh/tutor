import datetime

from sqlalchemy import ForeignKey

from app import db
from app.util.api_response import date_to_json


class Rate(db.Model):
    __tablename__ = 'rate'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    star = db.Column(db.Integer, nullable=False)
    content = db.Column(db.Text, nullable=True)

    user_id = db.Column(db.Integer, ForeignKey('users.id'))
    author_id = db.Column(db.Integer, ForeignKey('users.id'))

    created_date = db.Column(db.DateTime, nullable=True)
    updated_date = db.Column(db.DateTime, nullable=True)

    def __init__(self, star, content, user_id, author_id):
        self.star = star
        self.content = content
        self.user_id = user_id
        self.author_id = author_id
        self.created_date = datetime.datetime.now()
        self.updated_date = datetime.datetime.now()

    def to_json(self):
        return {
            'id': self.id,
            'star': self.star,
            'content': self.content,
            'created_date': date_to_json(self.created_date),
            'updated_date': date_to_json(self.updated_date),
            'user': self.user.to_json()
        }
