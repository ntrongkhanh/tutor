from flask_restx import Namespace, fields

from .base_dto import base
from .. import app
from ..util.auth_parser_util import get_auth_required_parser


class RateDto:
    api = Namespace('Rate', description="Rate")
    __base = api.model("base", base)

    """ request"""
    rate_request = get_auth_required_parser(api)
    rate_request.add_argument("star", type=int, location="args", required=True)
    rate_request.add_argument("content", type=str, location="args", required=False)

    filter_request = get_auth_required_parser(api)
    filter_request.add_argument("page", type=int, location="args", required=False, default=app.config['DEFAULT_PAGE'])
    filter_request.add_argument("page_size", type=int, location="args", required=False,
                                default=app.config['DEFAULT_PAGE_SIZE'])
    """response"""
    message_response = api.inherit('message_response', base, {
        'data': fields.String,
    })
