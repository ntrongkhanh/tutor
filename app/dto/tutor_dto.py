from flask_restx import Namespace, fields

from app.dto.base_dto import base


class TutorDto:
    api = Namespace('Tutor', description="Tutor")

    filter_request = api.model('filter', {
        'id': fields.Integer(required=False, description='description'),
        'description': fields.String(required=False, description='description'),

    })

    filter_request = api.model('filter', {
        'id': fields.Integer(required=False, description='description'),
        'description': fields.String(required=False, description='description'),

    })

    image_data = api.inherit('image_data', {
        'description': fields.String(required=False, description='description'),
        'created_date': fields.DateTime(required=False, description='description'),
        'updated_date': fields.DateTime(required=False, description='description'),
        'data': fields.String(required=False, description='description'),
    })

    image_response = api.inherit('login_response', base, {
        'data': fields.Nested(image_data)
    })
