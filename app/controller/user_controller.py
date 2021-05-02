from flask import request
from flask_restx import Resource

from app.dto.user_dto import UserDto
from app.model.user_model import User
from app.service import user_service as service
from app.util.api_response import response_object

# create
# create_parser = api.parser()
# create_parser.add_argument("id", type=int, location='id', required=True)
# create_parser.add_argument("username", type=str, location='username', required=True)
# create_parser.add_argument("password", type=str, location='password', required=True)
#
api = UserDto.api
_create = UserDto.user_creation_request


@api.route("/create")
class create(Resource):
    @api.doc('create user')
    @api.expect(_create, validate=True)
    @api.marshal_with(UserDto.create_response)
    def post(self):
        args = request.json

        data = service.create_user(args)


        # create_success_response=DemoDTO.create_success_response
        return response_object(data=data)
