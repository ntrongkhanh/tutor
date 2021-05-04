import datetime

from flask import json
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from app import db
from app.util.api_response import json_serial


class Image(db.Model):
    __tablename__ = 'image'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.String(255), nullable=True)
    data = db.Column(db.LargeBinary(length=(2 ** 32) - 1), nullable=True)

    # user = relationship("User", uselist=False, backref="avatar")
    user = relationship("User", backref="avatar", lazy=True, uselist=False)
    tutor_id = db.Column(db.Integer, ForeignKey('tutor.id'))

    created_date = db.Column(db.DateTime, nullable=True)
    updated_date = db.Column(db.DateTime, nullable=True)

    # tutor = relationship("Tutor", backref="images", lazy=True)

    def __init__(self, description, data, tutor_id=0):
        self.description = description
        self.data = data
        if tutor_id != 0:
            self.tutor_id = tutor_id
        self.created_date = datetime.datetime.now()
        self.updated_date = datetime.datetime.now()

    def to_json(self):
        return {
            'id': self.id,
            'description': self.description,
            'created_date':self.created_date, #json.dumps(self.created_date, default=json_serial),
            'updated_date':self.updated_date, #json.dumps(self.updated_date, default=json_serial),
            'data': self.data,
        }
