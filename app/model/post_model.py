from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from app import db


class Post(db.Model):
    __tablename__ = 'post'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    is_tutor = db.Column(db.Boolean, default=False, nullable=False)
    title = db.Column(db.String(255), nullable=True)
    description = db.Column(db.String(255), nullable=True)
    teaching_address = db.Column(db.String(255), nullable=True)
    subject = db.Column(db.String(255), nullable=True)
    class_type = db.Column(db.String(255), nullable=True)
    other_information = db.Column(db.String(255), nullable=True)
    fee = db.Column(db.String(255), nullable=True)
    schedule = db.Column(db.String(255), nullable=True)
    number_of_sessions = db.Column(db.String(255), nullable=True)
    require = db.Column(db.String(255), nullable=True)
    contact = db.Column(db.String(255), nullable=True)

    user_id = db.Column(db.Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="posts")
