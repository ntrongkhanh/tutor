from flask_restx import Namespace, fields, inputs

from app.dto.base_dto import base
from .user_dto import UserDto
from .. import app
from ..util.auth_parser_util import get_auth_required_parser, get_auth_not_required_parser


class PostDto:
    api = Namespace('Post', description="Post")
    """request"""
    create_parser = get_auth_required_parser(api)
    create_parser.add_argument("title", type=str, location="json", required=True)
    create_parser.add_argument("description", type=str, location="json", required=False)
    create_parser.add_argument("teaching_address", type=str, location="json", required=False)
    create_parser.add_argument("subject", type=str, location="json", required=True)
    create_parser.add_argument("class_type", type=str, location="json", required=False)
    create_parser.add_argument("other_information", type=str, location="json", required=False)
    create_parser.add_argument("fee", type=int, location="json", required=True)
    create_parser.add_argument("schedule", type=str, location="json", required=False)
    create_parser.add_argument("number_of_sessions", type=str, location="json", required=False)
    create_parser.add_argument("require", type=str, location="json", required=False)
    create_parser.add_argument("contact", type=str, location="json", required=False)
    create_parser.add_argument("form_of_teaching", type=str, location="json", required=False)

    update_parser = get_auth_required_parser(api)
    update_parser.add_argument("id", type=int, location="json", required=True)
    update_parser.add_argument("title", type=str, location="json", required=False)
    update_parser.add_argument("description", type=str, location="json", required=False)
    update_parser.add_argument("teaching_address", type=str, location="json", required=False)
    update_parser.add_argument("subject", type=str, location="json", required=False)
    update_parser.add_argument("class_type", type=str, location="json", required=False)
    update_parser.add_argument("other_information", type=str, location="json", required=False)
    update_parser.add_argument("fee", type=int, location="json", required=False)
    update_parser.add_argument("schedule", type=str, location="json", required=False)
    update_parser.add_argument("number_of_sessions", type=str, location="json", required=False)
    update_parser.add_argument("require", type=str, location="json", required=False)
    update_parser.add_argument("contact", type=str, location="json", required=False)
    update_parser.add_argument("form_of_teaching", type=str, location="json", required=False)

    filter_parser = get_auth_not_required_parser(api)
    filter_parser.add_argument("id", type=int, location="args", required=False)
    filter_parser.add_argument("is_tutor", type=inputs.boolean, location="args", required=False)
    filter_parser.add_argument("title", type=str, location="args", required=False)
    filter_parser.add_argument("description", type=str, location="args", required=False)
    filter_parser.add_argument("teaching_address", type=str, location="args", required=False)
    filter_parser.add_argument("subject", type=str, location="args", required=False)
    filter_parser.add_argument("class_type", type=str, location="args", required=False)
    filter_parser.add_argument("other_information", type=str, location="args", required=False)
    filter_parser.add_argument("fee", type=int, location="args", required=False)
    filter_parser.add_argument("schedule", type=str, location="args", required=False)
    filter_parser.add_argument("number_of_sessions", type=str, location="args", required=False)
    filter_parser.add_argument("require", type=str, location="args", required=False)
    filter_parser.add_argument("contact", type=str, location="args", required=False)
    filter_parser.add_argument("form_of_teaching", type=str, location="args", required=False)
    filter_parser.add_argument("user_id", type=int, location="args", required=False)
    filter_parser.add_argument("user_name", type=str, location="args", required=False)
    filter_parser.add_argument("page", type=int, location="args", required=False, default=app.config['DEFAULT_PAGE'])
    filter_parser.add_argument("page_size", type=int, location="args", required=False,
                                default=app.config['DEFAULT_PAGE_SIZE'])
    """data"""

    post_data = api.inherit('post_data', {
        'id': fields.Integer(required=False, description='description'),
        'is_tutor': fields.Boolean(required=False, description='description'),
        'title': fields.String(required=False, description='description'),
        'description': fields.String(required=False, description='description'),
        'teaching_address': fields.String(required=False, description='description'),
        'subject': fields.String(required=False, description='description'),
        'class_type': fields.String(required=False, description='description'),
        'other_information': fields.String(required=False, description='description'),
        'fee': fields.String(required=False, description='description'),
        'schedule': fields.String(required=False, description='description'),
        'number_of_sessions': fields.String(required=False, description='description'),
        'require': fields.String(required=False, description='description'),
        'contact': fields.String(required=False, description='description'),
        'form_of_teaching': fields.String(required=False, description='description'),
        'created_date': fields.String(required=False, description='description'),
        'updated_date': fields.String(required=False, description='description'),
        'user': fields.Nested(UserDto.user_data, required=False, description='description')
    })
    pagination_data = api.model('pagination', {
        'page': fields.Integer,
        'total': fields.Integer,
    })
    """response"""

    post_response = api.inherit('post_response', base, {
        'data': fields.Nested(post_data)
    })
    post_list_response = api.inherit('post_list_response', base, {
        'data': fields.List(fields.Nested(post_data)),
        'pagination': fields.Nested(pagination_data),
    })

    message_response = api.inherit('message_response', base, {
        'data': fields.String,
    })
