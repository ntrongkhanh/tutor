from datetime import datetime
from operator import or_

from flask import request
from flask_restx import Resource
from werkzeug.datastructures import FileStorage

from app.dto.user_dto import UserDto
from app.model.user_model import User
from app.service import user_service
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

        args = request.form
        file = request.files['file']

        return user_service.create_user(args, file)


_update_parser = api.parser()
_update_parser.add_argument("email", type=str, location='json', required=True)
_update_parser.add_argument("first_name", type=str, location='json', required=True)
_update_parser.add_argument("last_name", type=str, location='json', required=True)
_update_parser.add_argument("sex", type=bool, location='json', required=True)
_update_parser.add_argument("birthday", type=datetime, location='json', required=True)


# coi lại cái lấy từ parser

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
        # args = _update_parser.parse_args()
        args = request.json
        return user_service.update_user(args, 1)
        # cần bổ sung token, truyên user id vào


# chưa làm

_active_parser = api.parser()
_active_parser.add_argument("email", type=str, location='args', required=True)
_active_parser.add_argument("code", type=str, location='args', required=True)


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
        pass
        # args=_active_parser.parse_args()
        #
        # return user_service.active_user(args)


@api.response('/active')
class Active(Resource):
    @api.doc('active account')
    @api.response(401, 'Unauthorized')
    @api.response(403, 'Forbidden')
    @api.response(404, 'Not found')
    @api.response(500, 'Internal server error')
    def get(self):
        args = _active_parser.parse_args()

        return user_service.active_user(args)


_filter_parser = api.parser()
_filter_parser.add_argument("email", type=str, location='args', required=False)
_filter_parser.add_argument("first_name", type=str, location='args', required=False)
_filter_parser.add_argument("last_name", type=str, location='args', required=False)
_filter_parser.add_argument("sex", type=bool, location='args', required=False)
_filter_parser.add_argument("birthday", type=datetime, location='args', required=False)
_filter_parser.add_argument("page", type=int, location="args", required=False, default=1)
_filter_parser.add_argument("page_size", type=int, location="args", required=False, default=10)
_filter_response = UserDto.user_list_response


# chưa làm


@api.route('/')
class Filter(Resource):
    @api.doc('filter user')
    @api.response(500, 'Internal server error')
    @api.expect(_filter_parser, validate=True)
    @api.marshal_with(_filter_response, 200)
    def get(self):
        """filter users"""
        args = _filter_parser.parse_args()
        page = args['page']
        page_size = args['page_size']
        users = User.query.filter(
            or_(User.email.like("%{}%".format(args['email'])), args['email'] is None),
            or_(User.first_name.like("%{}%".format(args['first_name'])), args['first_name'] is None),
            or_(User.last_name.like("%{}%".format(args['last_name'])), args['last_name'] is None),
            or_(User.sex == args['last_name'], args['sex'] is None),
            or_(User.birthday == args['birthday'], args['birthday'] is None),
            User.is_active
        ).paginate(page, page_size, error_out=False)

        return response_object(data=[user.to_json() for user in users.items],
                               pagination={'total': users.total, 'page': users.page}), 200


_user_response = UserDto.user_response


# chưa làm

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

    # jwt required , truyền user id vào


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
        return user_service.get_profile(1)


_update_avatar_parser = api.parser()
_update_avatar_parser.add_argument("file", type=FileStorage, location="files", required=True)
_update_avatar_parser.add_argument("user_id", type=int, location='form', required=True)


# còn jwt


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
        user_id = request.form['user_id']
        file = request.files['file']
        return user_service.update_avatar(file, user_id)


_change_password_parser = api.parser()
_change_password_parser.add_argument("new_password", type=str, location='json', required=False)
_change_password_parser.add_argument("old_password", type=str, location='json', required=False)


# coi lại cái lấy từ parser
# cần jwt, truyên user id vào

@api.route('/password/change')
class ChangePassword(Resource):
    @api.doc('change password')
    @api.response(401, 'Unauthorized')
    @api.response(403, 'Forbidden')
    @api.response(404, 'Not found')
    @api.response(500, 'Internal server error')
    @api.expect(_change_password_parser, validate=True)
    @api.marshal_with(_message_response, 200)
    def post(self):
        """change password"""
        # args = _change_password_parser.parse_args()
        args = request.json
        return user_service.change_password(args, 1)


_forgot_password_parser = api.parser()
_forgot_password_parser.add_argument("email", type=str, location='args', required=False)


# maybe
@api.route('/password/forgot')
class ForgotPassword(Resource):
    @api.doc('forgot password')
    @api.response(401, 'Unauthorized')
    @api.response(403, 'Forbidden')
    @api.response(404, 'Not found')
    @api.response(500, 'Internal server error')
    @api.expect(_forgot_password_parser, validate=True)
    @api.marshal_with(_message_response, 200)
    def get(self):
        """forgot password"""
        email = _forgot_password_parser.parse_args()['email']
        return user_service.forgot_password(email)


_reset_parser = api.parser()
_reset_parser.add_argument("email", type=str, location='args', required=True)
_reset_parser.add_argument("code", type=str, location='args', required=True)
_reset_parser.add_argument("password", type=str, location='json', required=True)


# coi lại cái lấy từ parser


@api.route('/password/reset')
@api.param('email')
class Reset(Resource):
    @api.doc('reset password')
    @api.response(401, 'Unauthorized')
    @api.response(403, 'Forbidden')
    @api.response(404, 'Not found')
    @api.response(500, 'Internal server error')
    @api.expect(_reset_parser, validate=True)
    @api.marshal_with(_message_response)
    def post(self):
        """reset password"""
        args = _reset_parser.parse_args()
        password = request.json
        return user_service.reset_password(args, password)
