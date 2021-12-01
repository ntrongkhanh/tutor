from datetime import datetime

from sqlalchemy import ForeignKey

from app import db
from app.util.api_response import date_to_json


class Class(db.Model):
    __tablename__ = 'class'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    post_id = db.Column(db.Integer, ForeignKey('post.id'))

    student_id = db.Column(db.Integer, ForeignKey('users.id'), nullable=True)
    teacher_id = db.Column(db.Integer, ForeignKey('users.id'), nullable=True)

    student = db.relationship("User", backref="students", uselist=False, foreign_keys=[student_id])
    teacher = db.relationship("User", backref="teachers", uselist=False, foreign_keys=[teacher_id])

    created_date = db.Column(db.DateTime, nullable=True)

    def __init__(self, post_id, student_id, teacher_id):
        self.post_id = post_id
        self.student_id = student_id
        self.teacher_id = teacher_id
        self.created_date = datetime.now()

    def to_json(self):
        return {
            'id': self.id,
            'post': self.post.to_json(),
            'student': self.student.to_json(),
            'teacher': self.teacher.to_json(),
            'created_date': date_to_json(self.created_date)
        }
