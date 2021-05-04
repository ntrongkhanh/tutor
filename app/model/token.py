import datetime
from app import db


class Token(db.Model):
    __tablename__ = 'token'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(500), unique=True, nullable=False)
    created_date = db.Column(db.DateTime, nullable=True)

    def __init__(self, token):
        self.token = token
        self.blacklisted_on = datetime.datetime.now()

    def __repr__(self):
        return '<id: token: {}'.format(self.token)

    @staticmethod
    def check_token(auth_token):
        # check whether auth token has been blacklisted
        res = Token.query.filter_by(token=str(auth_token)).first()
        if res:
            return True
        else:
            return False
