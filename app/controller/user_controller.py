from operator import or_

from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restx import Resource

import app.util.response_message as message
from app.dto.user_dto import UserDto
from app.model.code_model import Code
from app.model.user_model import User
from app.service import user_service
from app.util import response_message
from app.util.api_response import response_object
from app.util.auth_parser_util import get_auth_required_parser

api = UserDto.api

_message_response = UserDto.message_response

_update_parser = UserDto.update_parser

_filter_parser = UserDto.filter_parser
_filter_response = UserDto.user_list_response

_user_response = UserDto.user_response

_create_parser = UserDto.create_parser


@api.route('')
class UserListController(Resource):

    # tạm ok
    @api.doc('create user')
    @api.expect(_create_parser, validate=True)
    # @api.marshal_with(_message_response, 201)
    def post(self):
        """create user (Tạo tài khoản)"""

        args = _create_parser.parse_args()

        return user_service.create_user(args)

    # coi lại cái lấy từ parser
    # truyền jwt
    @api.doc('update user')
    @api.expect(_update_parser, validate=True)
    # @api.marshal_with(_message_response, 200)
    @jwt_required()
    def put(self):
        """update user"""
        # args = _update_parser.parse_args()
        args = _update_parser.parse_args()
        user_id = get_jwt_identity()['user_id']
        return user_service.update_user(args, user_id)

    # tạm
    @api.doc('filter user')
    @api.expect(_filter_parser, validate=True)
    # @api.marshal_with(_filter_response, 200)
    def get(self):
        """filter users"""
        args = _filter_parser.parse_args()
        page = args['page']
        page_size = args['page_size']
        is_tutor = True if args['is_tutor'] == 'true' or args['is_tutor'] else False

        users = User.query.filter(
            or_(User.email.like("%{}%".format(args['email'])), args['email'] is None),
            or_(User.first_name.like("%{}%".format(args['first_name'])), args['first_name'] is None),
            or_(User.last_name.like("%{}"
                                    "%".format(args['last_name'])), args['last_name'] is None),
            or_(User.sex == args['last_name'], args['sex'] is None),
            or_(User.is_tutor == is_tutor, args['is_tutor'] is None),
            # or_(User.birthday == args['birthday'], args['birthday'] is None),
            User.is_active
        ).paginate(page, page_size, error_out=False)

        return response_object(data=[user.to_json() for user in users.items],
                               pagination={'total': users.total, 'page': users.page}), 200


# chưa làm


@api.route('/inactive/<user_id>')
class Inactive(Resource):
    @api.doc('inactive')
    # @api.marshal_with(_message_response, 200)
    def get(self, user_id):
        """inactive user"""
        pass
        # args=_active_parser.parse_args()
        #
        # return user_service.active_user(args)


_active_parser = UserDto.active_parser


# ok
@api.route('/active')
class Active(Resource):
    @api.doc('active account')
    @api.expect(_active_parser, validate=True)
    def get(self):
        args = _active_parser.parse_args()

        return user_service.active_user(args)


_get_parser = get_auth_required_parser(api)


# chưa làm

@api.route('/<user_id>')
class GetById(Resource):
    @api.doc('get by id')
    @api.expect(_get_parser, validate=True)
    # @api.marshal_with(_user_response, 200)
    def get(self, user_id):
        """get by id user"""
        return get_by_id(user_id)


def get_by_id(user_id):
    user = User.query.get(user_id)
    if not user:
        return response_object(status=False, message=response_message.USER_NOT_FOUND), 404
    return response_object(data=user.to_json()), 200


_profile_parser = get_auth_required_parser(api)


# jwt required , truyền user id vào

@api.route('/profile')
class Profile(Resource):
    @api.doc('profile')
    @api.expect(_profile_parser, validate=True)
    # #@api.marshal_with(_user_response, 200)
    @jwt_required()
    def get(self):
        """get profile"""

        user_id = get_jwt_identity()['user_id']

        return user_service.get_profile(user_id)


_update_avatar_parser = UserDto.update_avatar_parser


# còn jwt


@api.route('/update-avatar')
class UpdateAvatar(Resource):
    @api.doc('update avatar')
    @api.expect(_update_avatar_parser, validate=True)
    # @api.marshal_with(_message_response, 200)
    @jwt_required()
    def put(self):
        """update avatar"""
        user_id = get_jwt_identity()['user_id']
        file = request.files['file']
        return user_service.update_avatar(file, user_id)


_change_password_parser = UserDto.change_password_parser


# coi lại cái lấy từ parser
# cần jwt, truyên user id vào

@api.route('/password/change')
class ChangePassword(Resource):
    @api.doc('change password')
    @api.expect(_change_password_parser, validate=True)
    # @api.marshal_with(_message_response, 200)
    @jwt_required()
    def post(self):
        """change password"""
        # args = _change_password_parser.parse_args()
        user_id = get_jwt_identity()['user_id']
        args = request.json
        return user_service.change_password(args, user_id)


_forgot_password_parser = UserDto.forgot_password_parser


# maybe
@api.route('/password/forgot')
class ForgotPassword(Resource):
    @api.doc('forgot password')
    @api.expect(_forgot_password_parser, validate=True)
    # @api.marshal_with(_message_response, 200)
    def get(self):
        """forgot password"""
        email = _forgot_password_parser.parse_args()['email']

        return user_service.forgot_password(email)


_reset_parser = UserDto.reset_parser


# coi lại cái lấy từ parser


@api.route('/password/reset')
class Reset(Resource):
    @api.doc('reset password')
    @api.expect(_reset_parser, validate=True)
    # @api.marshal_with(_message_response, 200)
    def post(self):
        """reset password"""
        args = _reset_parser.parse_args()
        password = request.json['password']
        return user_service.reset_password(args, password)


_check_code_parser = UserDto.check_code_parser


@api.route('/code/check')
class CheckCode(Resource):
    @api.doc('check code')
    @api.expect(_check_code_parser, validate=True)
    # @api.marshal_with(_message_response, 200)
    def post(self):
        """check code"""
        args = _check_code_parser.parse_args()

        reset_code = Code.query.filter_by(email=args['email']).first()
        if not reset_code:
            return response_object(status=False, message=message.NOT_FOUND_404), 404
        if reset_code.code != args['code']:
            return response_object(status=False, message=message.NOT_FOUND_404), 404

        return response_object(), 200
