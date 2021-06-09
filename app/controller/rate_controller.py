from flask_jwt_extended import jwt_required
from flask_restx import Resource

import app.util.response_message as response_message
from app.dto.rate_dto import RateDto
from app.util.auth_parser_util import get_auth_required_parser

api = RateDto.api

_rate_request = RateDto.rate_request


@api.route('/<user_id>')
class RateController(Resource):
    @api.doc('rate user')
    @api.expect(_rate_request, validate=True)
    @api.marshal_with(response_message, 201)
    @api.response(201, 'Created')
    @api.response(401, 'Unauthorized')
    @api.response(403, 'Forbidden')
    @api.response(404, 'Not found')
    @api.response(500, 'Internal server error')
    @jwt_required()
    def post(self, user_id):
        pass

    @api.doc('update rate')
    @api.expect(_rate_request, validate=True)
    @api.marshal_with(response_message, 201)
    @api.response(200, 'Success')
    @api.response(401, 'Unauthorized')
    @api.response(403, 'Forbidden')
    @api.response(404, 'Not found')
    @api.response(500, 'Internal server error')
    @jwt_required()
    def put(self, user_id):
        pass

    @api.doc('delete rate')
    @api.expect(get_auth_required_parser(api), validate=True)
    @api.marshal_with(response_message, 201)
    @api.response(200, 'Success')
    @api.response(401, 'Unauthorized')
    @api.response(403, 'Forbidden')
    @api.response(404, 'Not found')
    @api.response(500, 'Internal server error')
    @jwt_required()
    def delete(self, user_id):
        pass
