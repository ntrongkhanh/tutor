import datetime
from app import db


class BlacklistToken(db.Model):
    __tablename__ = 'black-list-token'

    token = db.Column(db.String(500), primary_key=True)

    # @staticmethod
    # def check_token(auth_token):
    #     # check whether auth token has been blacklisted
    #     res = BlacklistToken.query.filter_by(token=str(auth_token)).first()
    #     if res:
    #         return True
    #     else:
    #         return False
