from datetime import datetime

from sqlalchemy import ForeignKey

from app import db
from app.model.model_enum import RegistrationStatus
from app.util.api_response import date_to_json


class Registration(db.Model):
    __tablename__ = 'registration'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    status = db.Column(db.Enum(RegistrationStatus), default=RegistrationStatus.PENDING, nullable=True)

    post_id = db.Column(db.Integer, ForeignKey('post.id'))
    registrant_id = db.Column(db.Integer, ForeignKey('users.id'))

    created_date = db.Column(db.DateTime, nullable=True)
    updated_date = db.Column(db.DateTime, nullable=True)

    def __init__(self, post_id, student_id):
        self.post_id = post_id
        self.student_id = student_id
        self.status = RegistrationStatus.PENDING
        self.created_date = datetime.now()
        self.updated_date = datetime.now()

    def to_json(self):
        return {
            'id': self.id,
            'status': self.star,
            'post_id': self.content,
            'student_id': self.created_date,
            'created_date': date_to_json(self.created_date),
            'updated_date': date_to_json(self.updated_date)
        }