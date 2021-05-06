from flask_restx import Resource

from app.dto.tutor_dto import TutorDto
from app.util.api_response import response_object

api = TutorDto.api


@api.route('/create')
class create(Resource):
    @api.doc('create tutor')
    def post(self):
        return None


@api.route('/update')
class update(Resource):
    @api.doc('update tutor')
    def put(self):
        return None


@api.route('/delete/<id>')
class delete(Resource):
    @api.doc('delete tutor')
    def delete(self):
        return response_object(), 200


@api.route('/')
class filter(Resource):
    @api.doc('filter tutor')
    def get(self):
        return None


@api.route('/<id>')
class get(Resource):
    @api.doc('get tutor by id')
    def get(self):
        return None
