import re

from flask_jwt_extended import create_access_token, get_jwt
from sqlalchemy import func

import app.util.response_message as message
from app import app, db
from app.model.black_list_token import BlacklistToken
from app.model.user_model import User
from app.util import response_message
from app.util.api_response import response_object


def login(args):
    valid = validate_email_and_password(args['email'], args['password'])
    if not isinstance(valid, bool):
        return valid
    user = User.query.filter(func.lower(User.email) == func.lower(args['email'])).first()
    if not user:
        return response_object(status=False, message=response_message.EMAIL_NOT_EXISTS), 401
    if not user.is_active:
        return response_object(status=False, message=response_message.ACCOUNT_IS_NOT_ACTIVATED), 401
    if not user.verify_password(args['password']):
        return response_object(status=False, message=response_message.PASSWORD_WRONG), 401
    auth_token = create_access_token(identity=user.to_payload(), expires_delta=app.config['TOKEN_EXPIRED_TIME'])
    if auth_token:
        data = user.to_json()
        data['token'] = auth_token
        return response_object(data=data), 200
    return response_object(status=False, message=response_message.UNAUTHORIZED_401), 401


def logout(auth_token):
    jti = get_jwt()["jti"]
    if auth_token:
        black_list = BlacklistToken(token=jti)
        db.session.add(black_list)
        db.session.commit()

    return response_object(), 200


def check(user_id):
    user = User.query.get(user_id)
    if not user:
        return response_object(status=False, message=response_message.UNAUTHORIZED_401), 401

    auth_token = create_access_token(identity=user.to_payload(), expires_delta=app.config['TOKEN_EXPIRED_TIME'])
    if auth_token:
        data = user.to_json_tutor()
        data['token'] = auth_token
        return response_object(data=data), 200
    return response_object(status=False, message=response_message.UNAUTHORIZED_401), 401


def validate_email_and_password(email, password):
    if not validate_email(email):
        return response_object(status=False, message=message.INVALID_EMAIL), 400
    if not validate_password(password):
        return response_object(status=False, message=message.INVALID_PASSWORD), 400

    return True


def validate_password(password):
    if len(password) < app.config['MIN_PASSWORD_CHARACTERS']:
        return False
    return True


def validate_email(email):
    regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
    if not re.search(regex, email):
        return False
    return True
