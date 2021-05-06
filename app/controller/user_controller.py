from datetime import timedelta, datetime

import flask
from flask import request
from flask_jwt_extended import create_access_token
from flask_restx import Resource
from werkzeug.datastructures import FileStorage

from app import bcrypt, app
from app.dto.user_dto import UserDto
from app.model.user_model import User
from app.service import user_service as service

api = UserDto.api
_create_request = UserDto.user_creation_request
_update_request = UserDto.user_update_request
_login_request = UserDto.login_request

_login_response = UserDto.login_response
_profile_response = UserDto.profile_response

create_parser = api.parser()
create_parser.add_argument("file", type=FileStorage, location="files", required=True)
create_parser.add_argument("email", type=str, location='form', required=True)
create_parser.add_argument("password", type=str, location='form', required=True)
create_parser.add_argument("first_name", type=str, location='form', required=True)
create_parser.add_argument("last_name", type=str, location='form', required=True)
create_parser.add_argument("sex", type=bool, location='form', required=True)
create_parser.add_argument("birthday", type=datetime, location='form', required=True)


@api.route("/create")
class create(Resource):
    @api.doc('create user')
    @api.expect(create_parser, validate=True)
    def post(self):
        args = request.form
        file = request.files['file']
        return service.create_user(args, file)


@api.route("/update")
class update(Resource):
    @api.doc('update user')
    @api.expect(_update_request, validate=True)
    def put(self):
        args = request.json
        return service.update_user(args, 1)


active_parser = api.parser()
active_parser.add_argument("email", type=str, location='args', required=True)
active_parser.add_argument("code", type=str, location='args', required=True)


@api.route("/active/")
class active(Resource):
    @api.doc('active mail')
    @api.expect(active_parser, validate=True)
    def get(self):
        args = active_parser.parse_args()
        return service.active_user(args)


@api.route("/login/")
class login(Resource):
    @api.doc('login mail')
    @api.expect(_login_request, validate=True)
    @api.marshal_with(_login_response, 200)
    def post(self):
        args = request.json
        return service.login(args)


@api.route("/profile")
class profile(Resource):
    @api.doc('profile')
    # @api.expect(_profile_response, validate=True)
    @api.marshal_with(_profile_response, 200)
    def get(self):
        # args = request.json
        return service.get_profile(1)


@api.route("/login1/")
class login1(Resource):
    @api.doc('login1 mail')
    @api.expect(_login_request, validate=True)
    # @api.marshal_with(_login_response, 200)
    def post(self):
        # get the post data
        post_data = request.json
        try:
            # fetch the user data
            user = User.query.filter_by(email=post_data.get('email')).first()
            if not user:
                return flask.make_response('không tồn tại tài khoản')
            if bcrypt.check_password_hash(user.password, post_data.get('password')):
                # auth_token = user.encode_auth_token(user.id, user.is_admin, user.is_tutor)
                expires = timedelta(days=10)

                auth_token = create_access_token(identity=user.to_payload(), expires_delta=expires)

                if auth_token:
                    response = flask.make_response(auth_token)
                    return response
            else:
                return flask.make_response('sai mật khẩu')
        except Exception as e:
            print(e)
            return flask.make_response('thất bại')


checkapi = api.parser()
checkapi.add_argument("Authorization", type=str, location="headers", required=True)


@api.route("/check/")
class check(Resource):
    @api.doc("check")
    @api.expect(checkapi, validate=True)
    def get(self):
        args = checkapi.parse_args()
        token = args["Authorization"].split(" ")[1]

        resp = 0
        if token:
            resp = User.decode_auth_token(token)

        user = User.query.filter(User.id == resp).first()

        responseObject = {
            'status': 'success',
            'data': {
                'user_id': user.id,
                'email': user.is_admin,
                'admin': user.is_tutor,
                'registered_on': user.created_date
            }
        }
        print(responseObject)
        return flask.make_response('a')
