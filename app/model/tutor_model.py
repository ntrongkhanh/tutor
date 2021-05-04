import json
import datetime

from sqlalchemy.orm import relationship

from app import db
from app.util.api_response import json_serial


class Tutor(db.Model):
    __tablename__ = 'tutor'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    birthday = db.Column(db.DateTime, nullable=True)
    career = db.Column(db.String(255), nullable=True)
    tutor_description = db.Column(db.Text, nullable=True)
    majors = db.Column(db.String(255), nullable=True)
    degree = db.Column(db.String(255), nullable=True)
    school = db.Column(db.String(255), nullable=True)
    address = db.Column(db.String(255), nullable=True)
    subject = db.Column(db.String(255), nullable=True)
    class_type = db.Column(db.String(255), nullable=True)
    experience = db.Column(db.String(255), nullable=True)
    other_information = db.Column(db.String(255), nullable=True)
    is_active = db.Column(db.Boolean, default=False, nullable=False)

    images = relationship("Image", backref="tutor", lazy=True)

    created_date = db.Column(db.DateTime, nullable=True)
    updated_date = db.Column(db.DateTime, nullable=True)

    def __init__(self, birthday, career, tutor_description, majors, degree, school, address, class_type, experience,
                 other_information):
        self.birthday = birthday
        self.career = career
        self.tutor_description = tutor_description
        self.majors = majors
        self.degree = degree
        self.school = school
        self.address = address
        self.class_type = class_type
        self.experience = experience
        self.other_information = other_information
        self.created_date = datetime.datetime.now()
        self.updated_date = datetime.datetime.now()

    def to_json(self):
        return {
            'id': self.id,
            'birthday': json.dumps(self.birthday, default=json_serial),
            'career': self.career,
            'tutor_description': self.tutor_description,
            'majors': self.majors,
            'degree': self.degree,
            'school': self.school,
            'address': self.address,
            'subject': self.subject,
            'class_type': self.class_type,
            'experience': self.experience,
            'other_information': self.other_information,
            'images': [image for image in self.images],
            'created_date': json.dumps(self.created_date, default=json_serial),
            'updated_date': json.dumps(self.updated_date, default=json_serial)
        }
