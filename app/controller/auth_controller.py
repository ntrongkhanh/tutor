import re

from flask import request
from flask_jwt_extended import jwt_required, create_access_token, get_jwt, get_jwt_identity
from flask_restx import Resource
from sqlalchemy import func

import app.util.response_message as message
from app import app, db
from app.dto.auth_dto import AuthDto
from app.model.black_list_token import BlacklistToken
from app.model.user_model import User
from app.util import response_message
from app.util.api_response import response_object
from app.util.auth_parser_util import get_auth_required_parser

api = AuthDto.api
_message_response = AuthDto.message_response

_login_parser = api.parser()
_login_parser.add_argument("email", type=str, location="json", required=True)
_login_parser.add_argument("password", type=str, location="json", required=True)

_login_response = AuthDto.login_response


# tạm ok
@api.route('/login')
class Login(Resource):
    @api.doc('login ')
    @api.expect(_login_parser, validate=True)
    @api.response(401, 'Unauthorized')
    @api.response(404, 'Not found')
    @api.marshal_with(_login_response, code=200)
    def post(self):
        """Login (Đăng nhập)"""
        args = request.json
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


# tạm ok
@api.route('/logout')
class Logout(Resource):
    @api.doc('logout')
    @jwt_required()
    @api.expect(get_auth_required_parser(api), validate=True)
    @api.response(401, 'Unauthorized')
    @api.marshal_with(_message_response, 200)
    def get(self):
        """Logout (Đăng xuất)"""
        # jti = get_jwt()["jti"]
        # jwt_redis_blocklist.set(jti, "", ex=app.config['TOKEN_EXPIRED_TIME'])
        # return response_object(), 200
        auth_token = request.headers['Authorization'].split(" ")[1]
        jti = get_jwt()["jti"]
        if auth_token:
            black_list = BlacklistToken(token=jti)
            db.session.add(black_list)
            db.session.commit()

        # jwt_redis_blocklist

        return response_object(), 200


_check_token_parser = api.parser()


@api.route('/check')
class CheckToken(Resource):
    @api.doc('check Token expiration time')
    @api.expect(get_auth_required_parser(api), validate=True)
    @api.response(401, 'Unauthorized')
    @api.marshal_with(_login_response, 200)
    @jwt_required()
    def get(self):
        """Check token (Kiểm tra hạn của token)"""

        user = User.query.get(get_jwt_identity()['user_id'])
        if not user:
            return response_object(status=False, message=response_message.UNAUTHORIZED_401), 401

        auth_token = create_access_token(identity=user.to_payload(), expires_delta=app.config['TOKEN_EXPIRED_TIME'])
        if auth_token:
            data = user.to_json()
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
