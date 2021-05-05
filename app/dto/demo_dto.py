from flask_restx import Namespace, fields

from .base_dto import base


class DemoDTO:
    api = Namespace('Demo', description="Demo")
    __base = api.model("base", base)

    demo_request = api.model('demo', {
        'username': fields.String(required=True, description='user email address'),
        'password': fields.String(required=True, description='user password'),

    })

    file_content_data = api.inherit('create_data', {
        'id': fields.Integer,
        'username': fields.String,
        'password': fields.String
    })

    aa = api.inherit('create_data', {
        'text': fields.String,
    })

    create_success_response = api.inherit('create_success', base, {
        'data': fields.Nested(aa)
    })

    update_success_response = api.inherit('update_success', base, {
        'data': fields.Nested(file_content_data)
    })

    delete_success_response = api.inherit('Delele success', base, {
        "data": fields.Nested(None)
    })
