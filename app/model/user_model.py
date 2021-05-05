import json
from datetime import datetime, timedelta

import jwt
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from app import db, bcrypt, app
from app.model.token import Token
from app.util.api_response import json_serial


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(255), nullable=True)
    last_name = db.Column(db.String(255), nullable=True)
    sex = db.Column(db.Boolean, default=True, nullable=True)
    is_tutor = db.Column(db.Boolean, default=False, nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    is_active = db.Column(db.Boolean, default=False, nullable=False)

    avatar_id = db.Column(db.Integer, ForeignKey('image.id'), nullable=True)

    # avatar = relationship("Image", backref="user", lazy=True)
    posts = relationship("Post", backref="user", lazy=True)
    search_history = relationship("SearchHistory", backref="user", lazy=True)

    created_date = db.Column(db.DateTime, nullable=True)
    updated_date = db.Column(db.DateTime, nullable=True)

    def __init__(self, email, password, first_name, last_name, sex, avatar_id):
        self.email = email
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
        self.first_name = first_name
        self.last_name = last_name
        self.sex = sex
        self.avatar_id = avatar_id
        self.is_tutor = False
        self.is_admin = False
        self.is_active = False
        self.created_date = datetime.now()
        self.updated_date = datetime.now()

    def encode_auth_token(self, user_id, is_admin, is_tutor):
        """
        Generates the Auth Token    .strftime("%d-%m-%Y %H:%M:%S"),
        :return: string         json.dumps((datetime.utcnow() + timedelta(days=1)), default=json_serial),
        """
        try:
            payload = {
                "expired_time": json.dumps((datetime.utcnow() + timedelta(days=1)), default=json_serial),
                "issued_at": json.dumps(datetime.utcnow(), default=json_serial),
                "user_id": user_id,
                "admin": is_admin,
                "tutor": is_tutor
            }

            return jwt.encode(
                payload,
                app.config.get('SECRET_KEY'),
                algorithm="HS256"
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Validates the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'), algorithms=["HS256"])
            is_blacklisted_token = Token.check_token(auth_token)
            if is_blacklisted_token:
                return 'Token blacklisted. Please log in again.'
            else:
                return payload['user_id']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'

    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def to_json(self):
        return {
            'id': self.id,
            'email': self.email,
            'first_name': self.last_name,
            'last_name': self.last_name,
            'sex': self.sex,
            'is_tutor': self.is_tutor,
            'is_admin': self.is_admin,
            'is_active': self.is_active,
            'avatar_id': self.avatar_id,
            'avatar': self.avatar,
            'created_date': self.created_date  # json.dumps(self.created_date, default=json_serial),
        }


def myconverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()
