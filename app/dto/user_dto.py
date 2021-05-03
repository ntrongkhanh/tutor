from flask_restx import Namespace, fields

from .base_dto import base


class UserDto:
    api = Namespace('User', description="User")
    __base = api.model("base", base)

    login_request = api.model('login', {
        'email': fields.String(required=True, description='user email address'),
        'password': fields.String(required=True, description='user password'),
    })

    user_creation_request = api.model('create', {
        'email': fields.String(required=False, description='user email address'),
        'password': fields.String(required=False, description='user email address'),
        'first_name': fields.String(required=False, description='user email address'),
        'last_name': fields.String(required=False, description='user email address'),
        'sex': fields.Boolean(required=False, description='user email address'),
    })

    user_update_request = api.model('update', {
        'first_name': fields.String(required=False, description='user email address'),
        'last_name': fields.String(required=False, description='user email address'),
        'sex': fields.Boolean(required=False, description='user email address')
    })

    avatar = api.inherit('avatar', {
        'id': fields.Integer(required=False, description='user email address'),
        'description': fields.String(required=False, description='user email address'),
        'data': fields.String(required=False, description='user email address'),
    })

    login_data = api.inherit('login', {
        'email': fields.String(required=False, description='user email address'),
        'first_name': fields.String(required=False, description='user email address'),
        'last_name': fields.String(required=False, description='user email address'),
        'sex': fields.Boolean(required=False, description='user email address'),
        'is_tutor': fields.Boolean(required=False, description='user email address'),
        'avatar_id': fields.Integer(required=False, description='user email address'),
        'avatar': fields.Nested(avatar),
        'token': fields.String(required=False, description='user email address')
    })

    login_response = api.inherit('login_success', base, {
        'data': fields.Nested(login_data)
    })

    active_response = api.inherit('active_success', base, {
        'data': 'active success'
    })

    reset_password_response = api.inherit('reset_password_success', base, {
        'data': 'active password success'
    })

    logout_response = api.inherit('logout_success', base, {
        'data': 'logout success'
    })

    change_password_response = api.inherit('change_password_success', base, {
        'data': 'change password success'
    })
