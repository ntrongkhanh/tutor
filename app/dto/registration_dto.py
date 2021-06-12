from flask_restx import Namespace, fields,inputs

from .base_dto import base
from .. import app
from ..util.auth_parser_util import get_auth_required_parser


class RegistrationDto:
    api = Namespace('Registration', description="Registration")
    __base = api.model("base", base)

    """request"""
    create_request = get_auth_required_parser(api)
    create_request.add_argument("post_id", type=int, location="args", required=True)
    create_request.add_argument("is_looking_for_tutor", type=bool, location="args", required=True)
    create_request.add_argument("user_id", type=int, location="args", required=True)


    # update_request = get_auth_required_parser(api)
    # create_request.add_argument("post_id", type=int, location="args", required=True)
    # create_request.add_argument("is_looking_for_tutor", type=bool, location="args", required=True)
    # create_request.add_argument("user_id", type=int, location="args", required=True)
    # create_request.add_argument("author_id", type=int, location="args", required=True)

    filter_request = get_auth_required_parser(api)
    filter_request.add_argument("post_id", type=int, location="args", required=True)
    filter_request.add_argument("is_looking_for_tutor", type=bool, location="args", required=True)
    filter_request.add_argument("user_id", type=int, location="args", required=True)
    filter_request.add_argument("author_id", type=int, location="args", required=True)
    filter_request.add_argument("page", type=int, location="args", required=False, default=app.config['DEFAULT_PAGE'])
    filter_request.add_argument("page_size", type=int, location="args", required=False,
                                default=app.config['DEFAULT_PAGE_SIZE'])

    """response"""
    message_response = api.inherit('message_response', base, {
        'data': fields.String,
    })