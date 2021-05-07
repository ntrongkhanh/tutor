from flask_restx import Namespace, fields

from app.dto.base_dto import base
from .user_dto import UserDto


class PostDto:
    api = Namespace('Post', description="Post")

    """data"""

    post_data = api.inherit('post_data', {
        'id': fields.Integer(required=False, description='description'),
        'is_tutor': fields.Boolean(required=False, description='description'),
        'title': fields.String(required=False, description='description'),
        'description': fields.String(required=False, description='description'),
        'teaching_address': fields.String(required=False, description='description'),
        'subject': fields.String(required=False, description='description'),
        'class_type': fields.String(required=False, description='description'),
        'other_information': fields.String(required=False, description='description'),
        'fee': fields.String(required=False, description='description'),
        'schedule': fields.String(required=False, description='description'),
        'number_of_sessions': fields.String(required=False, description='description'),
        'require': fields.String(required=False, description='description'),
        'contact': fields.String(required=False, description='description'),
        'form_of_teaching': fields.String(required=False, description='description'),
        'created_date': fields.String(required=False, description='description'),
        'updated_date': fields.String(required=False, description='description'),
        'user': fields.Nested(UserDto.login_data, required=False, description='description')
    })

    """response"""

    post_response = api.inherit('post_response', base, {
        'data': fields.Nested(post_data)
    })
    post_list_response = api.inherit('post_list_response', base, {
        'data': fields.List(fields.Nested(post_data))
    })

    message_response = api.inherit('get_saved_resume_list_response', base, {
        'data': fields.String,
    })
