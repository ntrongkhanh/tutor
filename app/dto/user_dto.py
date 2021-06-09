from flask_restx import Namespace, fields
from werkzeug.datastructures import FileStorage

from .base_dto import base
# from .tutor_dto import TutorDto
from .. import app
from ..util.auth_parser_util import get_auth_required_parser


class UserDto:
    api = Namespace('User', description="User")
    __base = api.model("base", base)
    """request"""
    create_parser = api.parser()
    # create_parser.add_argument("file", type=FileStorage, location="files", required=True)
    create_parser.add_argument("email", type=str, location='json', required=True)
    create_parser.add_argument("password", type=str, location='json', required=True)
    create_parser.add_argument("first_name", type=str, location='json', required=True)
    create_parser.add_argument("last_name", type=str, location='json', required=True)
    create_parser.add_argument("sex", type=bool, location='json', required=True)
    # create_parser.add_argument("birthday", type=datetime, location='form', required=True)

    update_parser = get_auth_required_parser(api)
    update_parser.add_argument("email", type=str, location='json', required=True)
    update_parser.add_argument("first_name", type=str, location='json', required=True)
    update_parser.add_argument("last_name", type=str, location='json', required=True)
    update_parser.add_argument("sex", type=bool, location='json', required=True)
    # update_parser.add_argument("birthday", type=datetime, location='json', required=True)

    filter_parser = get_auth_required_parser(api)
    filter_parser.add_argument("email", type=str, location='args', required=False)
    filter_parser.add_argument("first_name", type=str, location='args', required=False)
    filter_parser.add_argument("last_name", type=str, location='args', required=False)
    filter_parser.add_argument("sex", type=bool, location='args', required=False)
    # filter_parser.add_argument("birthday", type=datetime, location='args', required=False)
    filter_parser.add_argument("page", type=int, location="args", required=False, default=app.config['DEFAULT_PAGE'])
    filter_parser.add_argument("page_size", type=int, location="args", required=False,
                               default=app.config['DEFAULT_PAGE_SIZE'])

    active_parser = api.parser()
    active_parser.add_argument("email", type=str, location='args', required=True)
    active_parser.add_argument("code", type=str, location='args', required=True)

    update_avatar_parser = get_auth_required_parser(api)
    update_avatar_parser.add_argument("file", type=FileStorage, location="files", required=True)

    change_password_parser = get_auth_required_parser(api)
    change_password_parser.add_argument("new_password", type=str, location='json', required=False)
    change_password_parser.add_argument("old_password", type=str, location='json', required=False)

    forgot_password_parser = api.parser()
    forgot_password_parser.add_argument("email", type=str, location='args', required=False)

    reset_parser = api.parser()
    reset_parser.add_argument("email", type=str, location='args', required=True)
    reset_parser.add_argument("code", type=str, location='args', required=True)
    reset_parser.add_argument("password", type=str, location='json', required=True)

    check_code_parser = api.parser()
    check_code_parser.add_argument("email", type=str, location='args', required=True)
    check_code_parser.add_argument("code", type=str, location='args', required=True)
    """data"""

    image = api.inherit('image', {
        'id': fields.Integer(required=False, description='user email address'),
        'description': fields.String(required=False, description='user email address'),
    })

    login_data = api.inherit('login_data', {
        'email': fields.String(required=False, description='user email address'),
        'first_name': fields.String(required=False, description='user email address'),
        'last_name': fields.String(required=False, description='user email address'),
        'sex': fields.Boolean(required=False, description='user email address'),
        'is_tutor': fields.Boolean(required=False, description='user email address'),
        'is_admin': fields.Boolean(required=False, description='user email address'),
        'avatar_id': fields.Integer(required=False, description='user email address'),
        'token': fields.String(required=False, description='user email address'),
        'created_date': fields.String(required=False, description='user email address')
    })

    tutor_data = api.inherit('tutor_data', {
        'id': fields.Integer(required=False, description='description'),
        'public_id': fields.String(required=False, description='description'),
        'career': fields.String(required=False, description='description'),
        'tutor_description': fields.String(required=False, description='description'),
        'majors': fields.String(required=False, description='description'),
        'degree': fields.String(required=False, description='description'),
        'school': fields.String(required=False, description='description'),
        'city_address': fields.String(required=False, description='description'),
        'district_address': fields.String(required=False, description='description'),
        'detailed_address': fields.String(required=False, description='description'),
        'subject': fields.String(required=False, description='description'),
        'class_type': fields.String(required=False, description='description'),
        'experience': fields.String(required=False, description='description'),
        'other_information': fields.String(required=False, description='description'),
        'images': fields.Nested(image),
        'created_date': fields.String(required=False, description='description'),
        'updated_date': fields.String(required=False, description='description'),
        'status': fields.String(required=False, description='description'),
    })
    user_data = api.inherit('user_data', {
        'id': fields.Integer(required=False, description='user email address'),
        'email': fields.String(required=False, description='user email address'),
        'first_name': fields.String(required=False, description='user email address'),
        'last_name': fields.String(required=False, description='user email address'),
        'sex': fields.Boolean(required=False, description='user email address'),
        'average_rating': fields.Float(required=False, description='user email address'),
        'is_tutor': fields.Boolean(required=False, description='user email address'),
        'avatar_id': fields.Integer(required=False, description='user email address'),
        'tutor': fields.Nested(tutor_data),
        'created_date': fields.String(required=False, description='user email address'),
        'updated_date': fields.String(required=False, description='user email address')
    })
    profile_data = api.inherit('profile_data', {
        'id': fields.Integer(required=False, description='user email address'),
        'email': fields.String(required=False, description='user email address'),
        'first_name': fields.String(required=False, description='user email address'),
        'last_name': fields.String(required=False, description='user email address'),
        'sex': fields.Boolean(required=False, description='user email address'),
        'average_rating': fields.Float(required=False, description='user email address'),
        'is_tutor': fields.Boolean(required=False, description='user email address'),
        'avatar_id': fields.Integer(required=False, description='user email address'),
        'tutor': fields.Nested(tutor_data),
        'created_date': fields.String(required=False, description='user email address'),
        'updated_date': fields.String(required=False, description='user email address')
    })
    pagination_data = api.model('pagination', {
        'page': fields.Integer,
        'total': fields.Integer,
    })
    """response"""

    profile_response = api.inherit('profile_response', base, {
        'data': fields.Nested(profile_data)
    })

    login_response = api.inherit('login_response', base, {
        'data': fields.Nested(login_data)
    })

    user_response = api.inherit('user_response', base, {
        'data': fields.Nested(profile_data)
    })

    user_list_response = api.inherit('user_list_response', base, {
        'data': fields.List(fields.Nested(profile_data)),
        'pagination': fields.Nested(pagination_data)
    })

    message_response = api.inherit('message_response', base, {
        'data': fields.String,
    })
