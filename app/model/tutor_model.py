import datetime

from sqlalchemy.orm import relationship

from app import db
from app.model.image_model import Image
from app.model.model_enum import TutorStatus, enum_to_json
from app.util.api_response import date_to_json


class Tutor(db.Model):
    __tablename__ = 'tutor'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    public_id = db.Column(db.String(50), unique=True)

    career = db.Column(db.String(255), nullable=True)
    tutor_description = db.Column(db.Text, nullable=True)
    majors = db.Column(db.String(255), nullable=True)
    degree = db.Column(db.String(255), nullable=True)
    school = db.Column(db.String(255), nullable=True)

    city_address = db.Column(db.String(255), nullable=True)
    district_address = db.Column(db.String(255), nullable=True)
    detailed_address = db.Column(db.String(255), nullable=True)
    latitude = db.Column(db.String(255), nullable=True)
    longitude = db.Column(db.String(255), nullable=True)

    subject = db.Column(db.String(255), nullable=True)
    class_type = db.Column(db.String(255), nullable=True)
    experience = db.Column(db.Text, nullable=True)
    other_information = db.Column(db.Text, nullable=True)
    is_active = db.Column(db.Boolean, default=False, nullable=False)
    status = db.Column(db.Enum(TutorStatus), default=TutorStatus.PENDING, nullable=True)

    images = relationship("Image", backref="tutor", lazy=True)
    user = relationship("User", backref="tutor", lazy=True, uselist=False)

    created_date = db.Column(db.DateTime, nullable=True)
    updated_date = db.Column(db.DateTime, nullable=True)

    def __init__(self, public_id, career, tutor_description, majors, degree, school, subject, class_type,
                 experience, other_information, city_address, district_address,
                 detailed_address, latitude=None, longitude=None):
        self.public_id = public_id
        self.career = career
        self.tutor_description = tutor_description
        self.majors = majors
        self.degree = degree
        self.school = school
        self.city_address = city_address
        self.district_address = district_address
        self.detailed_address = detailed_address
        self.latitude = latitude
        self.longitude = longitude
        self.subject = subject
        self.class_type = class_type
        self.experience = experience
        self.other_information = other_information
        self.is_active = True
        self.created_date = datetime.datetime.now()
        self.updated_date = datetime.datetime.now()
        self.status = TutorStatus.APPROVED

    def to_json(self):
        return {
            'id': self.id,
            'public_id': self.public_id,
            'career': self.career,
            'tutor_description': self.tutor_description,
            'majors': self.majors,
            'degree': self.degree,
            'school': self.school,
            'city_address': self.city_address,
            'district_address': self.district_address,
            'detailed_address': self.detailed_address,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'subject': self.subject,
            'class_type': self.class_type,
            'experience': self.experience,
            'other_information': self.other_information,
            'images': Image.to_json_list(self.images),
            'created_date': date_to_json(self.created_date),
            'updated_date': date_to_json(self.updated_date),
            # 'user': self.user.to_json(),
            'status': enum_to_json(self.status, TutorStatus)
        }
