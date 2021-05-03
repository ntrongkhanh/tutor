from flask import request
from flask_restx import Resource

from app.dto.user_dto import UserDto
from app.service import user_service as service

# create
# create_parser = api.parser()
# create_parser.add_argument("id", type=int, location='id', required=True)
# create_parser.add_argument("username", type=str, location='username', required=True)
# create_parser.add_argument("password", type=str, location='password', required=True)
#
api = UserDto.api
_create_request = UserDto.user_creation_request
_update_request = UserDto.user_update_request


@api.route("/create")
class create(Resource):
    @api.doc('create user')
    @api.expect(_create_request, validate=True)
    def post(self):
        args = request.json

        return service.create_user(args)


@api.route("/update")
class update(Resource):
    @api.doc('update user')
    @api.expect(_update_request, validate=True)
    def put(self):
        args = request.json
        return service.update_user(args, 1)


@api.route("/send_mail")
class test_send_mail(Resource):
    @api.doc('send mail')
    def post(self):
        return service.test_send_mail()


active_parser = api.parser()
active_parser.add_argument("email", type=str, location='args', required=True)
active_parser.add_argument("code", type=str, location='args', required=True)


@api.route("/active/")
class active(Resource):
    @api.doc('send mail')
    @api.expect(active_parser, validate=True)
    def get(self):
        args = active_parser.parse_args()
        return service.active_user(args)
