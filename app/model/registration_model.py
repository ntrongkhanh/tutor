from datetime import datetime

from sqlalchemy import ForeignKey

from app import db
from app.model.model_enum import RegistrationStatus, enum_to_json
from app.util.api_response import date_to_json


class Registration(db.Model):
    __tablename__ = 'registration'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    status = db.Column(db.Enum(RegistrationStatus), default=RegistrationStatus.PENDING, nullable=True)
    is_read_by_approved_user = db.Column(db.Boolean, default=False, nullable=False)

    post_id = db.Column(db.Integer, ForeignKey('post.id'))

    # registrant_id = db.Column(db.Integer, ForeignKey('users.id'))
    """
    is_looking_for_tutor
    true:   author là người tìm gia sư
            user là gia sư nhận lớp
    false:  author là gia sư
            user là học viên                    
    """
    contact = db.Column(db.String(255), nullable=True)
    content = db.Column(db.Text, nullable=True)

    approved_user_id = db.Column(db.Integer, ForeignKey('users.id'), nullable=True)
    author_id = db.Column(db.Integer, ForeignKey('users.id'), nullable=True)

    approved_user = db.relationship("User", backref="approved_user", uselist=False, foreign_keys=[approved_user_id])
    author = db.relationship("User", backref="registration_author", uselist=False, foreign_keys=[author_id])

    created_date = db.Column(db.DateTime, nullable=True)
    updated_date = db.Column(db.DateTime, nullable=True)

    def __init__(self, post_id, approved_user_id, author_id, contact, content):
        self.post_id = post_id
        self.status = RegistrationStatus.PENDING
        self.approved_user_id = approved_user_id
        self.author_id = author_id
        self.contact = contact
        self.content = content
        self.created_date = datetime.now()
        self.updated_date = datetime.now()
        self.is_read_by_approved_user = False

    def get_status(self):
        return enum_to_json(self.status, RegistrationStatus)

    def to_json(self):
        return {
            'id': self.id,
            'status': enum_to_json(self.status, RegistrationStatus),
            'contact': self.contact,
            'content': self.content,
            'approved_user': self.approved_user.to_json(),
            'post': self.post.to_json(),
            'author': self.author.to_json(),
            'created_date': date_to_json(self.created_date),
            'updated_date': date_to_json(self.updated_date)
        }

    def to_json_with_read(self):
        return {
            'id': self.id,
            'status': enum_to_json(self.status, RegistrationStatus),
            'contact': self.contact,
            'content': self.content,
            'is_read': self.is_read_by_approved_user,
            'approved_user': self.approved_user.to_json(),
            'post': self.post.to_json(),
            'author': self.author.to_json(),
            'created_date': date_to_json(self.created_date),
            'updated_date': date_to_json(self.updated_date)
        }
