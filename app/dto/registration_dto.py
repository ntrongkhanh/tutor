from flask_restx import Namespace, fields

from .base_dto import base
from .. import app
from ..util.auth_parser_util import get_auth_required_parser


class RegistrationDto:
    api = Namespace('Registration', description="Registration")
    __base = api.model("base", base)

    """request"""
    create_request = get_auth_required_parser(api)
    create_request.add_argument("post_id", type=int, location="json", required=False)
    create_request.add_argument("contact", type=str, location="json", required=False)
    create_request.add_argument("content", type=str, location="json", required=False)

    # create_request.add_argument("approved_user_id", type=int, location="args", required=True)

    invite_request = get_auth_required_parser(api)
    invite_request.add_argument("content", type=str, location="json", required=False)
    invite_request.add_argument("title", type=str, location="json", required=True)
    invite_request.add_argument("description", type=str, location="json", required=False)
    invite_request.add_argument("city_address", type=str, location="json", required=False)
    invite_request.add_argument("district_address", type=str, location="json", required=False)
    invite_request.add_argument("detailed_address", type=str, location="json", required=False)
    invite_request.add_argument("latitude", type=str, location="json", required=False)
    invite_request.add_argument("longitude", type=str, location="json", required=False)
    invite_request.add_argument("subject", type=str, location="json", required=True)
    invite_request.add_argument("class_type", type=str, location="json", required=False)
    invite_request.add_argument("other_information", type=str, location="json", required=False)
    invite_request.add_argument("fee", type=int, location="json", required=True)
    invite_request.add_argument("schedule", type=str, location="json", required=False)
    invite_request.add_argument("number_of_sessions", type=str, location="json", required=False)
    invite_request.add_argument("require", type=str, location="json", required=False)
    invite_request.add_argument("contact", type=str, location="json", required=False)
    invite_request.add_argument("form_of_teaching", type=str, location="json", required=False)
    invite_request.add_argument("invited_user_id", type=int, location="args", required=True)

    # update_request = get_auth_required_parser(api)
    # create_request.add_argument("post_id", type=int, location="args", required=True)
    # create_request.add_argument("is_looking_for_tutor", type=bool, location="args", required=True)
    # create_request.add_argument("user_id", type=int, location="args", required=True)
    # create_request.add_argument("author_id", type=int, location="args", required=True)

    filter_request = get_auth_required_parser(api)
    filter_request.add_argument("status", type=str, location="args", required=False, default=None)
    filter_request.add_argument("page", type=int, location="args", required=False, default=app.config['DEFAULT_PAGE'])
    filter_request.add_argument("page_size", type=int, location="args", required=False,
                                default=app.config['DEFAULT_PAGE_SIZE'])

    """response"""
    message_response = api.inherit('message_response', base, {
        'data': fields.String,
    })
