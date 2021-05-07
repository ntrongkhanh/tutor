from datetime import datetime

from flask_restx import Resource
from werkzeug.datastructures import FileStorage

from app.dto.user_dto import UserDto
from app.util.api_response import response_object

api = UserDto.api

_message_response = UserDto.message_response

_create_parser = api.parser()
_create_parser.add_argument("file", type=FileStorage, location="files", required=True)
_create_parser.add_argument("email", type=str, location='form', required=True)
_create_parser.add_argument("password", type=str, location='form', required=True)
_create_parser.add_argument("first_name", type=str, location='form', required=True)
_create_parser.add_argument("last_name", type=str, location='form', required=True)
_create_parser.add_argument("sex", type=bool, location='form', required=True)
_create_parser.add_argument("birthday", type=datetime, location='form', required=True)


@api.route('/create')
class Create(Resource):
    @api.doc('create user')
    @api.response(201, 'Created')
    @api.response(401, 'Unauthorized')
    @api.response(403, 'Forbidden')
    @api.response(404, 'Not found')
    @api.response(500, 'Internal server error')
    @api.expect(_create_parser, validate=True)
    @api.marshal_with(_message_response, 201)
    def post(self):
        """create user (Tạo tài khoản)"""

        return response_object(), 201


_update_parser = api.parser()
_update_parser.add_argument("email", type=str, location='json', required=True)
_update_parser.add_argument("first_name", type=str, location='json', required=True)
_update_parser.add_argument("last_name", type=str, location='json', required=True)
_update_parser.add_argument("sex", type=bool, location='json', required=True)
_update_parser.add_argument("birthday", type=datetime, location='json', required=True)


@api.route('/update')
class Update(Resource):
    @api.doc('update user')
    @api.response(401, 'Unauthorized')
    @api.response(403, 'Forbidden')
    @api.response(404, 'Not found')
    @api.response(500, 'Internal server error')
    @api.expect(_update_parser, validate=True)
    @api.marshal_with(_message_response, 200)
    def put(self):
        """update user"""
        return response_object(), 200


@api.route('/inactive/<user_id>')
class Inactive(Resource):
    @api.doc('inactive')
    @api.response(401, 'Unauthorized')
    @api.response(403, 'Forbidden')
    @api.response(404, 'Not found')
    @api.response(500, 'Internal server error')
    @api.marshal_with(_message_response, 200)
    def get(self, user_id):
        """inactive user"""
        return response_object(), 200


_filter_parser = api.parser()
_filter_parser.add_argument("email", type=str, location='args', required=True)
_filter_parser.add_argument("first_name", type=str, location='args', required=True)
_filter_parser.add_argument("last_name", type=str, location='args', required=True)
_filter_parser.add_argument("sex", type=bool, location='args', required=True)
_filter_parser.add_argument("birthday", type=datetime, location='args', required=True)

_filter_response = UserDto.user_list_response


@api.route('/')
class Filter(Resource):
    @api.doc('filter user')
    @api.response(500, 'Internal server error')
    @api.expect(_filter_parser, validate=True)
    @api.marshal_with(_filter_response, 200)
    def get(self):
        """filter users"""
        return response_object(), 200


_user_response = UserDto.user_response


@api.route('/<user_id>')
class GetById(Resource):
    @api.doc('get by id')
    @api.response(401, 'Unauthorized')
    @api.response(403, 'Forbidden')
    @api.response(404, 'Not found')
    @api.response(500, 'Internal server error')
    @api.marshal_with(_user_response, 200)
    def get(self, user_id):
        """get by id user"""
        return response_object(), 200


@api.route('/profile')
class Profile(Resource):
    @api.doc('profile')
    @api.response(401, 'Unauthorized')
    @api.response(403, 'Forbidden')
    @api.response(404, 'Not found')
    @api.response(500, 'Internal server error')
    @api.marshal_with(_user_response, 200)
    def get(self):
        """get profile"""
        return response_object(), 200


@api.route('/update-avatar')
class UpdateAvatar(Resource):
    @api.doc('update avatar')
    @api.response(401, 'Unauthorized')
    @api.response(403, 'Forbidden')
    @api.response(404, 'Not found')
    @api.response(500, 'Internal server error')
    @api.marshal_with(_message_response, 200)
    def put(self):
        """update avatar"""
        return response_object(), 200


@api.route('/password/change')
class ChangePassword(Resource):
    @api.doc('change password')
    @api.response(401, 'Unauthorized')
    @api.response(403, 'Forbidden')
    @api.response(404, 'Not found')
    @api.response(500, 'Internal server error')
    @api.marshal_with(_message_response, 200)
    def post(self):
        """change password"""
        return response_object(), 200


@api.route('/password/forgot')
class ForgotPassword(Resource):
    @api.doc('forgot password')
    @api.response(401, 'Unauthorized')
    @api.response(403, 'Forbidden')
    @api.response(404, 'Not found')
    @api.response(500, 'Internal server error')
    @api.marshal_with(_message_response, 200)
    def get(self):
        """forgot password"""
        return response_object(), 200


@api.route('/password/reset')
class Rest(Resource):
    @api.doc('reset password')
    @api.response(401, 'Unauthorized')
    @api.response(403, 'Forbidden')
    @api.response(404, 'Not found')
    @api.response(500, 'Internal server error')
    @api.marshal_with(_message_response)
    def post(self):
        """reset password"""
        return response_object(), 200
