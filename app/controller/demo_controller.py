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
