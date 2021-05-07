import flask
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restx import Resource
from werkzeug.datastructures import FileStorage

from app import db
from app.dto.demo_dto import DemoDTO
from app.model.image_model import Image
from app.service import demo_service as service
from app.util.api_response import response_object
# create
# create_parser = api.parser()
# create_parser.add_argument("id", type=int, location='id', required=True)
# create_parser.add_argument("username", type=str, location='username', required=True)
# create_parser.add_argument("password", type=str, location='password', required=True)
#
from app.util.jwt_util import tutor_required, admin_required, HR_only

api = DemoDTO.api
_create = DemoDTO.demo_request


@api.route("/create")
class create(Resource):
    @api.doc('create demo')
    @api.expect(_create, validate=True)
    @api.marshal_with(DemoDTO.update_success_response)
    # @api.response(DemoDTO.create_success_response)
    def post(self):
        args = request.json

        data = service.create_demo(args)

        # create_success_response=DemoDTO.create_success_response
        text = {'text': type(args)}
        return response_object(data=data)


#
# upload = api.parser()
# upload.add_argument("file", type=FileStorage, location="files", required=True)
#
#
# @api.route('/upload-image')
# class upload(Resource):
#     @api.doc('upload')
#     @api.expect(upload,validate=True)
#     def post(selfs):
#         args = upload.parse_args()
#         file = args['file'].read()
#         image = Image(data=file, description='mô tả')
#         db.session.add(image)
#         db.session.commit()
#
#         return 'ok'

upload_parser = api.parser()
upload_parser.add_argument("file", type=FileStorage, location="files", required=True)
upload_parser.add_argument("code", type=str, location='form', required=True)


@api.route("/upload")
class upload(Resource):
    @api.doc('upload demo')
    @api.expect(upload_parser, validate=True)
    def post(self):
        args = upload_parser.parse_args()
        file = args['file'].read()
        file_name = args['code']
        image = Image(data=file, description=file_name)
        db.session.add(image)
        db.session.commit()

        return 'ok'


auth_parser = api.parser()
auth_parser.add_argument("Authorization", type=str, location='headers', required=True)


@api.route('/test-auth')
@api.expect(auth_parser)
class auth(Resource):
    @api.doc('auth')
    @api.expect(_create, validate=True)
    # @tutor_required()
    def post(self, user):
        print(user)
        return flask.make_response(user.first_name)


@api.route('/test-auth2')
@api.expect(auth_parser)
class auth2(Resource):
    @api.doc('auth2')
    # @jwt_required()
    # @html_tag_generator()
    @jwt_required()
    @admin_required()
    # @HR_only
    def get(self):
        identity = get_jwt_identity()
        print(identity['user_id'])
        return flask.make_response(str(identity['user_id']))
#
# create_parser = api.parser()
# create_parser.add_argument("file", type=FileStorage, location="files", required=True)
# create_parser.add_argument("email", type=str, location='form', required=True)
# create_parser.add_argument("password", type=str, location='form', required=True)
# create_parser.add_argument("first_name", type=str, location='form', required=True)
# create_parser.add_argument("last_name", type=str, location='form', required=True)
# create_parser.add_argument("sex", type=bool, location='form', required=True)
# create_parser.add_argument("birthday", type=datetime, location='form', required=True)
#
#
# @api.route("/create")
# class create(Resource):
#     @api.doc('create user')
#     @api.expect(create_parser, validate=True)
#     def post(self):
#         args = request.form
#         file = request.files['file']
#         return service.create_user(args, file)
#
#
# _update_request = UserDto.user_update_request
#
#
# @api.route("/update")
# class update(Resource):
#     @api.doc('update user')
#     @api.expect(_update_request, validate=True)
#     def put(self):
#         args = request.json
#         return service.update_user(args, 1)
#
#
# active_parser = api.parser()
# active_parser.add_argument("email", type=str, location='args', required=True)
# active_parser.add_argument("code", type=str, location='args', required=True)
#
#
# @api.route("/active")
# class active(Resource):
#     @api.doc('active mail')
#     @api.expect(active_parser, validate=True)
#     def get(self):
#         args = active_parser.parse_args()
#         return service.active_user(args)
#
#
# _login_request = UserDto.login_request
# _login_response = UserDto.login_response
#
#
# @api.route("/login")
# class login(Resource):
#     @api.doc('login mail')
#     @api.expect(_login_request, validate=True)
#     @api.marshal_with(_login_response, 200)
#     def post(self):
#         args = request.json
#         return service.login(args)
#
#
# _profile_response = UserDto.profile_response
#
#
# @api.route("/profile")
# class profile(Resource):
#     @api.doc('profile')
#     # @api.expect(_profile_response, validate=True)
#     @api.marshal_with(_profile_response, 200)
#     def get(self):
#         # args = request.json
#         return service.get_profile(1)
#
#
# """-------------------------------------------------------------------"""
#
#
# @api.route("/login1")
# class login1(Resource):
#     @api.doc('login1 mail')
#     @api.expect(_login_request, validate=True)
#     # @api.marshal_with(_login_response, 200)
#     def post(self):
#         # get the post data
#         post_data = request.json
#         try:
#             # fetch the user data
#             user = User.query.filter_by(email=post_data.get('email')).first()
#             if not user:
#                 return flask.make_response('không tồn tại tài khoản')
#             if bcrypt.check_password_hash(user.password, post_data.get('password')):
#                 # auth_token = user.encode_auth_token(user.id, user.is_admin, user.is_tutor)
#                 expires = timedelta(days=10)
#
#                 auth_token = create_access_token(identity=user.to_payload(), expires_delta=expires)
#
#                 if auth_token:
#                     response = flask.make_response(auth_token)
#                     return response
#             else:
#                 return flask.make_response('sai mật khẩu')
#         except Exception as e:
#             print(e)
#             return flask.make_response('thất bại')
#
#
# _check_api = api.parser()
# _check_api.add_argument("Authorization", type=str, location="headers", required=True)
#
#
# @api.route("/check")
# class check(Resource):
#     @api.doc("check")
#     @api.expect(_check_api, validate=True)
#     def get(self):
#         args = _check_api.parse_args()
#         token = args["Authorization"].split(" ")[1]
#
#         resp = 0
#         if token:
#             resp = User.decode_auth_token(token)
#
#         user = User.query.filter(User.id == resp).first()
#
#         responseObject = {
#             'status': 'success',
#             'data': {
#                 'user_id': user.id,
#                 'email': user.is_admin,
#                 'admin': user.is_tutor,
#                 'registered_on': user.created_date
#             }
#         }
#         print(responseObject)
#         return flask.make_response('a')
