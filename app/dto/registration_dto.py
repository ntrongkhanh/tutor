from flask_restx import Namespace, fields

from .base_dto import base
from ..util.auth_parser_util import get_auth_required_parser


class RegistrationDto:
    api = Namespace('Registration', description="Registration")
    __base = api.model("base", base)

    """response"""
    message_response = api.inherit('message_response', base, {
        'data': fields.String,
    })