from flask_restx import Namespace, fields

from .base_dto import base


class UserDto:
    api = Namespace('User', description="User")
    __base = api.model("base", base)

    """data"""

    avatar = api.inherit('avatar', {
        'id': fields.Integer(required=False, description='user email address'),
        'description': fields.String(required=False, description='user email address'),
    })

    login_data = api.inherit('login_data', {
        'email': fields.String(required=False, description='user email address'),
        'first_name': fields.String(required=False, description='user email address'),
        'last_name': fields.String(required=False, description='user email address'),
        'sex': fields.Boolean(required=False, description='user email address'),
        'is_tutor': fields.Boolean(required=False, description='user email address'),
        'avatar_id': fields.Integer(required=False, description='user email address'),
        'avatar': fields.Nested(avatar),
        'token': fields.String(required=False, description='user email address'),
        'created_date': fields.DateTime(required=False, description='user email address')
    })

    profile_data = api.inherit('profile_data', {
        'id': fields.Integer(required=False, description='user email address'),
        'email': fields.String(required=False, description='user email address'),
        'first_name': fields.String(required=False, description='user email address'),
        'last_name': fields.String(required=False, description='user email address'),
        'sex': fields.Boolean(required=False, description='user email address'),
        'is_tutor': fields.Boolean(required=False, description='user email address'),
        'avatar_id': fields.Integer(required=False, description='user email address'),
        'avatar': fields.Nested(avatar),
        'created_date': fields.DateTime(required=False, description='user email address')
    })

    """response"""

    profile_response = api.inherit('profile_response', base, {
        'data': fields.Nested(profile_data)
    })

    login_response = api.inherit('login_response', base, {
        'data': fields.Nested(login_data)
    })

    user_response = api.inherit('user_response', base, {
        'data': fields.Nested(profile_data)
    })

    user_list_response=api.inherit('user_list_response',base,{
        'data':fields.List(fields.Nested(profile_data))
    })

    message_response = api.inherit('get_saved_resume_list_response', base, {
        'data': fields.String,
    })
