from flask import request
from flask_restx import Resource

from app.dto.demo_dto import DemoDTO
from app.util.api_response import response_object
from app.service import demo_service as service

# create
# create_parser = api.parser()
# create_parser.add_argument("id", type=int, location='id', required=True)
# create_parser.add_argument("username", type=str, location='username', required=True)
# create_parser.add_argument("password", type=str, location='password', required=True)
#
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
        text = {'text':type(args)}
        return response_object(data=data)
