from flask_restx import Namespace, fields

from .base_dto import base


class AuthDto:
    api = Namespace('Auth', description="Auth")
    __base = api.model("base", base)

    """avatar"""
    _avatar_data = api.inherit('avatar_data', {
        'id': fields.Integer(required=False, description='description'),
        'description': fields.String(required=False, description='description'),
    })

    """ login """
    _login_data = api.inherit('login_data', {
        'id': fields.Integer(required=False, description='description'),
        'email': fields.String(required=False, description='description'),
        'first_name': fields.String(required=False, description='description'),
        'last_name': fields.String(required=False, description='description'),
        'birthday ': fields.DateTime(required=False, description='description'),
        'sex': fields.Boolean(required=False, description='description'),
        'is_tutor': fields.Boolean(required=False, description='description'),
        'is_admin': fields.Boolean(required=False, description='description'),
        'avatar_id': fields.Integer(required=False, description='description'),
        'avatar': fields.Nested(_avatar_data),
        'token': fields.String(required=False, description='description'),
    })

    login_response = api.inherit('login_response', base, {
        'data': fields.Nested(_login_data)
    })

    # message_response = api.inherit('message_response', base, {
    #     'data': fields.String(required=False, description='description')
    # })

    message_response = api.inherit('get_saved_resume_list_response', base, {
        'data': fields.String,
    })
