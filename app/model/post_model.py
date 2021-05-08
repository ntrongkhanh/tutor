import datetime

from sqlalchemy import ForeignKey

from app import db
from app.util.api_response import date_to_json


class Post(db.Model):
    __tablename__ = 'post'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    public_id = db.Column(db.String(50), unique=True)
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
    form_of_teaching = db.Column(db.String(255), nullable=True)
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    user_id = db.Column(db.Integer, ForeignKey('users.id'))
    # user = relationship("User", backref="posts")

    created_date = db.Column(db.DateTime, nullable=True)
    updated_date = db.Column(db.DateTime, nullable=True)

    def __init__(self, public_id, is_tutor, title, description, teaching_address, subject, class_type,
                 other_information, fee,
                 schedule, number_of_sessions, require, contact, form_of_teaching, user_id):
        self.public_id = public_id
        self.is_tutor = is_tutor
        self.title = title
        self.description = description
        self.teaching_address = teaching_address
        self.subject = subject
        self.class_type = class_type
        self.other_information = other_information
        self.fee = fee
        self.schedule = schedule
        self.number_of_sessions = number_of_sessions
        self.require = require
        self.contact = contact
        self.form_of_teaching = form_of_teaching
        self.user_id = user_id
        self.created_date = datetime.datetime.now()
        self.updated_date = datetime.datetime.now()

    def to_json(self):
        return {
            'id': self.id,
            'is_tutor': self.is_tutor,
            'title': self.title,
            'description': self.description,
            'teaching_address': self.teaching_address,
            'subject': self.subject,
            'class_type': self.class_type,
            'other_information': self.other_information,
            'fee': self.fee,
            'schedule': self.schedule,
            'number_of_sessions': self.number_of_sessions,
            'require': self.require,
            'contact': self.contact,
            'form_of_teaching': self.form_of_teaching,
            'user': self.user.to_json(),
            'created_date': date_to_json(self.created_date),
            'updated_date': date_to_json(self.updated_date),
        }
