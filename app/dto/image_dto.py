from flask_restx import Namespace, fields
from werkzeug.datastructures import FileStorage

from .base_dto import base
from .. import app
from ..util.auth_parser_util import get_auth_required_parser, get_auth_not_required_parser


class ImageDto:
    api = Namespace('Image', description="Image")
    """request"""
    create_parser = get_auth_required_parser(api)
    create_parser.add_argument("file", type=FileStorage, location="files", required=True)
    create_parser.add_argument("description", type=str, location='args', required=False)

    upload_parser = get_auth_required_parser(api)
    upload_parser.add_argument("file", type=FileStorage, location="files", required=True)
    upload_parser.add_argument("description", type=str, location='args', required=False)

    filter_parser = get_auth_not_required_parser(api)
    filter_parser.add_argument("id", type=int, location="args", required=False)
    filter_parser.add_argument("description", type=str, location="args", required=False)
    filter_parser.add_argument("page", type=int, location="args", required=False, default=app.config['DEFAULT_PAGE'])
    filter_parser.add_argument("page_size", type=int, location="args", required=False,
                               default=app.config['DEFAULT_PAGE_SIZE'])
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
