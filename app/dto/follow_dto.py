from flask_restx import Namespace

from .base_dto import base
from .. import app
from ..util.auth_parser_util import get_auth_required_parser


class FollowDto:
    api = Namespace('Follow', description="Follow")
    __base = api.model("base", base)

    """request"""
    filter_user_parser = get_auth_required_parser(api)
    filter_user_parser.add_argument("post_id", type=int, location='args', required=True)
    # filter_user_parser.add_argument("tutor", type=bool, location='args', required=False)
    filter_user_parser.add_argument("page", type=int, location="args", required=False, default=app.config['DEFAULT_PAGE'])
    filter_user_parser.add_argument("page_size", type=int, location="args", required=False,
                               default=app.config['DEFAULT_PAGE_SIZE'])

    filter_parser = get_auth_required_parser(api)
    filter_parser.add_argument("page", type=int, location="args", required=False, default=app.config['DEFAULT_PAGE'])
    filter_parser.add_argument("page_size", type=int, location="args", required=False,
                               default=app.config['DEFAULT_PAGE_SIZE'])