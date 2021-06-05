import datetime

from app import db


class Code(db.Model):
    __tablename__ = 'code'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), nullable=False)
    code = db.Column(db.String(255), nullable=False)

    created_date = db.Column(db.DateTime, nullable=True)

    def __init__(self, email, code):
        self.email = email
        self.code = code
        self.created_date = datetime.datetime.now()

