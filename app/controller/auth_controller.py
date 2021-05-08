from flask import request
from flask_jwt_extended import jwt_required, create_access_token
from flask_restx import Resource

from app import bcrypt, app
from app.dto.auth_dto import AuthDto
from app.model.user_model import User
from app.util.api_response import response_object
from app.util.auth_parser_util import get_auth_required_parser
from app.util import response_message

api = AuthDto.api
_message_response = AuthDto.message_response


_login_parser = api.parser()
_login_parser.add_argument("email", type=str, location="json", required=True)
_login_parser.add_argument("password", type=str, location="json", required=True)

_login_response = AuthDto.login_response


@api.route('/login')
class Login(Resource):
    @api.doc('login ')
    @api.expect(_login_parser, validate=True)
    @api.response(401, 'Unauthorized')
    @api.response(404, 'Not found')
    @api.marshal_with(_login_response, code=200)
    def post(self):
        """Login (Đăng nhập)"""
        args=request.json
        user=User.query.filter(User.email==args['email']).first()
        if not user:
            return response_object(status=False,message=response_message.EMAIL_ALREADY_EXISTS), 401
        if not user.verify_password(args['password']):
            return response_object(status=False, message=response_message.PASSWORD_WRONG), 401
        auth_token=create_access_token(identity=user.to_json(),expires_delta=app.config['TOKEN_EXPIRED_TIME'])
        if auth_token:
            data=user.to_json()
            data['token']=auth_token
            return response_object(data=data), 200
        return response_object(status=False,message=response_message.UNAUTHORIZED), 401

@api.route('/logout')
class Logout(Resource):
    @api.doc('logout')
    @jwt_required()
    @api.expect(get_auth_required_parser(api), validate=True)
    @api.response(401, 'Unauthorized')
    @api.marshal_with(_message_response, 200)
    def get(self):
        """Logout (Đăng xuất)"""
        return response_object(), 200


_check_token_parser = api.parser()


@api.route('/check')
class CheckToken(Resource):
    @api.doc('check Token expiration time')
    @api.expect(get_auth_required_parser(api), validate=True)
    @api.response(401, 'Unauthorized')
    @api.marshal_with(_message_response, 200)
    def get(self):
        """Check token (Kiểm tra hạn của token)"""
        return response_object(), 200
