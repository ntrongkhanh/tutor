import datetime

from app import db


class Code(db.Model):
    __tablename__ = 'code'

    email = db.Column(db.String(255), nullable=False, primary_key=True)
    code = db.Column(db.String(255), nullable=False)

    created_date = db.Column(db.DateTime, nullable=True)

    def __init__(self, email, code):
        self.email = email
        self.code = code
        self.created_date = datetime.datetime.now()
