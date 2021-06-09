from flask_restx import Namespace, fields

from .base_dto import base
from ..util.auth_parser_util import get_auth_required_parser


class ScheduleDto:
    api = Namespace('Schedule', description="Schedule")
    __base = api.model("base", base)

    """request"""
    create_request = get_auth_required_parser(api)
    create_request.add_argument("post_id", type=int, location="args", required=True)
    create_request.add_argument("day", type=int, location="args", required=True)
    create_request.add_argument("start_time", type=str, location="args", required=False)
    create_request.add_argument("end_time", type=str, location="args", required=False)

    update_request = get_auth_required_parser(api)
    update_request.add_argument("day", type=int, location="args", required=True)
    update_request.add_argument("start_time", type=str, location="args", required=False)
    update_request.add_argument("end_time", type=str, location="args", required=False)

    """response"""
    message_response = api.inherit('message_response', base, {
        'data': fields.String,
    })