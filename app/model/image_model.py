import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from app import db
from app.util.api_response import date_to_json


class Image(db.Model):
    __tablename__ = 'image'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.String(255), nullable=True)
    data = db.Column(db.LargeBinary(), nullable=True)
    link = db.Column(db.Text, nullable=True)
    is_public = db.Column(db.Boolean, default=True, nullable=False)

    # user = relationship("User", uselist=False, backref="avatar")
    user = relationship("User", backref="avatar", lazy=True, uselist=False)
    tutor_id = db.Column(db.Integer, ForeignKey('tutor.id'), nullable=True)

    created_date = db.Column(db.DateTime, nullable=True)
    updated_date = db.Column(db.DateTime, nullable=True)

    # tutor = relationship("Tutor", backref="images", lazy=True)

    def __init__(self, description, data, tutor_id=0, is_public=True):
        self.description = description
        self.data = data
        if tutor_id != 0:
            self.tutor_id = tutor_id
        self.created_date = datetime.datetime.now()
        self.updated_date = datetime.datetime.now()
        self.is_public = is_public
        self.link = None

    def to_json(self):
        return {
            'id': self.id,
            'description': self.description,
            'is_public': self.is_public,
            'created_date': date_to_json(self.created_date),
            'updated_date': date_to_json(self.updated_date)
        }

    @staticmethod
    def to_json_list(images):
        images = sorted(images, key=lambda x: x.id)
        return [image.to_json() for image in images]
