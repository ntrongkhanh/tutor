from flask_jwt_extended import jwt_required
from flask_restx import Resource

from app.dto.auth_dto import AuthDto
from app.util.api_response import response_object
from app.util.auth_parser_util import get_auth_required_parser

api = AuthDto.api

_login_parser = api.parser()
_login_parser.add_argument("email", type=str, location="json", required=True)
_login_parser.add_argument("password", type=str, location="json", required=True)

_login_response = AuthDto.login_response
_message_response = AuthDto.message_response


@api.route('/login')
class Login(Resource):
    @api.doc('login ')
    @api.expect(_login_parser, validate=True)
    @api.response(401, 'Unauthorized')
    @api.response(404, 'Not found')
    @api.marshal_with(_login_response, code=200)
    def post(self):
        """Login (Đăng nhập)"""
        return response_object(), 200


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
