import json
from datetime import datetime

import jwt
import pytz
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from app import db, bcrypt, app
from app.model.black_list_token import BlacklistToken
from app.util.api_response import json_serial, date_to_json


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(255), nullable=True)
    last_name = db.Column(db.String(255), nullable=True)
    birthday = db.Column(db.DateTime, nullable=True)
    sex = db.Column(db.Boolean, default=True, nullable=True)
    is_tutor = db.Column(db.Boolean, default=False, nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    is_active = db.Column(db.Boolean, default=False, nullable=False)

    avatar_id = db.Column(db.Integer, ForeignKey('image.id'), nullable=True)
    tutor_id = db.Column(db.Integer, ForeignKey('tutor.id'), nullable=True)

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

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    @staticmethod
    def encode_auth_token(user_id, is_admin, is_tutor):
        """
        Generates the Auth Token    .strftime("%d-%m-%Y %H:%M:%S"),
        :return: string         json.dumps((datetime.utcnow() + timedelta(days=1)), default=json_serial),
        """
        try:
            payload = {
                "expired_time": json.dumps((datetime.now() + app.config['TOKEN_EXPIRED_TIME']), default=json_serial),
                "issued_at": json.dumps(datetime.now(), default=json_serial),
                "user_id": user_id,
                "is_admin": is_admin,
                "is_tutor": is_tutor
            }
            auth_token = jwt.encode(
                payload,
                app.config.get('SECRET_KEY'),
                algorithm="HS256"
            )

            token = BlacklistToken(token=auth_token)
            db.session.add(token)
            db.session.commit()
            return auth_token
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

            token = BlacklistToken.query.filter(BlacklistToken.token == auth_token).first()

            # is_blacklisted_token = Token.check_token(auth_token)
            if not token:
                return 'Token blacklisted. Please log in again.'
            else:
                tz_London = pytz.timezone('Asia/Saigon')
                print(token.created_date + app.config.get("TOKEN_EXPIRED_TIME"))
                print(datetime.now())
                print((token.created_date + app.config.get("TOKEN_EXPIRED_TIME")) < datetime.now())
                print('aa')
                if (token.created_date + app.config.get("TOKEN_EXPIRED_TIME")) < datetime.now():
                    print('hết hạn')
                    db.session.delete(token)
                    db.session.commit()
                    return 'Signature expired. Please log in again.'
                return payload
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
            'first_name': self.first_name,
            'last_name': self.last_name,
            'birthday': date_to_json(self.birthday) if self.birthday else None,
            'sex': self.sex,
            'is_tutor': self.is_tutor,
            'is_admin': self.is_admin,
            'is_active': self.is_active,
            'avatar_id': self.avatar_id,
            # 'avatar': self.avatar.to_json(),
            'created_date': date_to_json(self.created_date)  # json.dumps(self.created_date, default=json_serial),
        }

    def to_payload(self):
        return {
            'user_id': self.id,
            'is_tutor': self.is_tutor,
            'is_admin': self.is_admin,
            'is_active': self.is_active,
        }


def myconverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()
