from flask_jwt_extended import create_access_token

from flask_jwt_extended import create_access_token

from app import app
from app.model.user_model import User
from app.util import response_message
from app.util.api_response import response_object


def login(email, password):
    user = User.query.filter(User.email == email).first()
    if not user:
        return response_object(status=False, message=response_message.EMAIL_ALREADY_EXISTS), 401
    if not user.is_active:
        return response_object(status=False, message=response_message.ACCOUNT_IS_NOT_ACTIVATED), 401
    if not user.verify_password(password):
        return response_object(status=False, message=response_message.PASSWORD_WRONG), 401
    auth_token = create_access_token(identity=user.to_payload(), expires_delta=app.config['TOKEN_EXPIRED_TIME'])
    if auth_token:
        data = user.to_json()
        data['token'] = auth_token
        return response_object(data=data), 200
    return response_object(status=False, message=response_message.UNAUTHORIZED), 401


def logout(token):
    pass


def check():
    pass
