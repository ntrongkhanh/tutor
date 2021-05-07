from flask_restx import Namespace, fields

from .base_dto import base


class ImageDto:
    api = Namespace('Image', description="Image")

    """data"""

    image_data = api.inherit('image_data', {
        'id': fields.Integer(required=False, description='description'),
        'description': fields.String(required=False, description='description'),
    })
    pagination_data = api.model('pagination', {
        'page': fields.Integer,
        'total': fields.Integer,
    })
    """response"""

    image_response = api.inherit('image_response', base, {
        'data': fields.Nested(image_data)
    })

    image_list_response = api.inherit('image_list_response', base, {
        'data': fields.List(fields.Nested(image_data)),
        'pagination': fields.Nested(pagination_data)
    })

    message_response = api.inherit('message_response', base, {
        'data': fields.String,
    })
