import datetime
import json

from sqlalchemy.orm import relationship

from app import db
from app.util.api_response import json_serial, date_to_json


class Tutor(db.Model):
    __tablename__ = 'tutor'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    public_id = db.Column(db.String(50), unique=True)
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

    def __init__(self, public_id, birthday, career, tutor_description, majors, degree, school, address, class_type,
                 experience, other_information):
        self.public_id = public_id
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
            'public_id': self.public_id,
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
            'created_date': date_to_json(self.created_date),
            'updated_date': date_to_json(self.updated_date)
        }
