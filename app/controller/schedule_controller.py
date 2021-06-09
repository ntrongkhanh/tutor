from flask_jwt_extended import jwt_required
from flask_restx import Resource

from app.dto.schedule_dto import ScheduleDto
from app.util import response_message
from app.util.auth_parser_util import get_auth_required_parser

api = ScheduleDto.api

_create_request = ScheduleDto.create_request


@api.route('')
class CreateScheduleController(Resource):
    @api.doc('create schedule')
    @api.expect(_create_request, validate=True)
    @api.marshal_with(response_message, 201)
    @api.response(201, 'Created')
    @api.response(401, 'Unauthorized')
    @api.response(403, 'Forbidden')
    @api.response(404, 'Not found')
    @api.response(500, 'Internal server error')
    @jwt_required()
    def post(self):
        pass


_update_request = ScheduleDto.update_request


@api.route('/<schedule_id>')
class RateController(Resource):
    @api.doc('get schedule')
    @api.marshal_with(response_message, 200)
    @api.response(200, 'Success')
    @api.response(401, 'Unauthorized')
    @api.response(403, 'Forbidden')
    @api.response(404, 'Not found')
    @api.response(500, 'Internal server error')
    @jwt_required()
    def get(self, schedule_id):
        pass

    @api.doc('update schedule')
    @api.expect(_update_request, validate=True)
    @api.marshal_with(response_message, 200)
    @api.response(200, 'Success')
    @api.response(401, 'Unauthorized')
    @api.response(403, 'Forbidden')
    @api.response(404, 'Not found')
    @api.response(500, 'Internal server error')
    @jwt_required()
    def put(self, schedule_id):
        pass

    @api.doc('delete schedule')
    @api.marshal_with(get_auth_required_parser(api), 200)
    @api.response(200, 'Success')
    @api.response(401, 'Unauthorized')
    @api.response(403, 'Forbidden')
    @api.response(404, 'Not found')
    @api.response(500, 'Internal server error')
    @jwt_required()
    def delete(self, schedule_id):
        pass
