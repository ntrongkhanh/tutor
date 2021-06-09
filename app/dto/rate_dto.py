from flask_restx import Namespace, fields

from .base_dto import base
from ..util.auth_parser_util import get_auth_required_parser


class RateDto:
    api = Namespace('Rate', description="Rate")
    __base = api.model("base", base)

    """ request"""
    rate_request=get_auth_required_parser(api)
    rate_request.add_argument("star", type=int, location="args", required=True)
    rate_request.add_argument("content", type=int, location="args", required=False)
