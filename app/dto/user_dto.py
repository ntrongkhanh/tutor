from flask_restx import Namespace, fields

from .base_dto import base


class UserDto:
    api = Namespace('User', description="User")
    __base = api.model("base", base)

    login_request = api.model('login_request', {
        'email': fields.String(required=True, description='user email address'),
        'password': fields.String(required=True, description='user password'),
    })

    user_creation_request = api.model('user_creation_request', {
        'email': fields.String(required=False, description='user email address'),
        'password': fields.String(required=False, description='user email address'),
        'first_name': fields.String(required=False, description='user email address'),
        'last_name': fields.String(required=False, description='user email address'),
        'sex': fields.Boolean(required=False, description='user email address'),
    })

    user_update_request = api.model('user_update_request', {
        'first_name': fields.String(required=False, description='user email address'),
        'last_name': fields.String(required=False, description='user email address'),
        'sex': fields.Boolean(required=False, description='user email address')
    })

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

    profile_response = api.inherit('profile_response', base, {
        'data': fields.Nested(profile_data)
    })

    login_response = api.inherit('login_response', base, {
        'data': fields.Nested(login_data)
    })

    active_response = api.inherit('active_response', base, {
        'data': 'active success'
    })

    reset_password_response = api.inherit('reset_password_response', base, {
        'data': 'active password success'
    })

    logout_response = api.inherit('logout_response', base, {
        'data': 'logout success'
    })

    change_password_response = api.inherit('change_password_response', base, {
        'data': 'change password success'
    })
