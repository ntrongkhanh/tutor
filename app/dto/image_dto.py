from flask_restx import Namespace, fields

from .base_dto import base


class ImageDto:
    api = Namespace('Image', description="Image")

    image_data = api.inherit('image_data', {
        'description': fields.String(required=False, description='user email address'),
        'created_date': fields.DateTime(required=False, description='user email address'),
        'updated_date': fields.DateTime(required=False, description='user email address'),
        'data': fields.String(required=False, description='user email address'),
    })

    image_response = api.inherit('login_response', base, {
        'data': fields.Nested(image_data)
    })
