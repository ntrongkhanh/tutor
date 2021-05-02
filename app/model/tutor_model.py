from datetime import datetime

from sqlalchemy.orm import relationship

from app import db


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
    join_date = db.Column(db.DateTime, default=datetime.now, nullable=False)

    images = relationship("Image", back_populates="tutor")
