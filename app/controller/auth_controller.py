from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restx import Resource

from app.dto.auth_dto import AuthDto
from app.service import auth_service
from app.util.auth_parser_util import get_auth_required_parser

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
    ##@api.marshal_with(_login_response, code=200)
    def post(self):
        """Login (Đăng nhập)"""
        args = request.json

        return auth_service.login(args)


# tạm ok
@api.route('/logout')
class Logout(Resource):
    @api.doc('logout')
    @api.expect(get_auth_required_parser(api), validate=True)
    ##@api.marshal_with(_message_response, 200)
    @jwt_required()
    def get(self):
        """Logout (Đăng xuất)"""
        auth_token = request.headers['Authorization'].split(" ")[1]
        return auth_service.logout(auth_token)


_check_token_parser = api.parser()


@api.route('/check')
class CheckToken(Resource):
    @api.doc('check Token expiration time')
    @api.expect(get_auth_required_parser(api), validate=True)
    @api.response(401, 'Unauthorized')
    ##@api.marshal_with(_login_response, 200)
    @jwt_required()
    def get(self):
        """Check token (Kiểm tra hạn của token)"""
        user_id = get_jwt_identity()['user_id']
        return auth_service.check(user_id)
