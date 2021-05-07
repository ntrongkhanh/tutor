from flask_restx import Namespace, fields

from app.dto.base_dto import base
from app.dto.user_dto import UserDto


class TutorDto:
    api = Namespace('Tutor', description="Tutor")

    """data"""

    tutor_data = api.inherit('tutor_data', {
        'public_id': fields.Integer(required=False, description='description'),
        'career': fields.String(required=False, description='description'),
        'tutor_description': fields.String(required=False, description='description'),
        'majors': fields.String(required=False, description='description'),
        'degree': fields.String(required=False, description='description'),
        'school': fields.String(required=False, description='description'),
        'address': fields.String(required=False, description='description'),
        'subject': fields.String(required=False, description='description'),
        'class_type': fields.String(required=False, description='description'),
        'experience': fields.String(required=False, description='description'),
        'other_information': fields.String(required=False, description='description'),
        'images': fields.String(required=False, description='description'),
        'user': fields.Nested(UserDto.login_data, required=False, description='description'),
        'created_date': fields.String(required=False, description='description'),
        'updated_date': fields.String(required=False, description='description'),
    })
    pagination_data = api.model('pagination', {
        'page': fields.Integer,
        'total': fields.Integer,
    })
    """response"""

    tutor_response = api.inherit('tutor_response', base, {
        'data': fields.Nested(tutor_data)
    })

    tutor_list_response = api.inherit('tutor_list_response', base, {
        'data': fields.List(fields.Nested(tutor_data)),
        'pagination':fields.Nested(pagination_data)
    })

    message_response = api.inherit('message_response', base, {
        'data': fields.String,
    })
