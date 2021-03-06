from flask_restx import Namespace, fields
from werkzeug.datastructures import FileStorage

from app import app
from app.dto.base_dto import base
from app.util.auth_parser_util import get_auth_required_parser, get_auth_not_required_parser


class TutorDto:
    api = Namespace('Tutor', description="Tutor")
    """request"""
    create_parser = get_auth_required_parser(api)
    create_parser.add_argument("career", type=str, location='json', required=False)
    create_parser.add_argument("tutor_description", type=str, location='json', required=False)
    create_parser.add_argument("majors", type=str, location='json', required=False)
    create_parser.add_argument("degree", type=str, location='json', required=False)
    create_parser.add_argument("subject", type=str, location='json', required=False)
    create_parser.add_argument("school", type=str, location='json', required=False)
    create_parser.add_argument("city_address", type=str, location='json', required=False)
    create_parser.add_argument("district_address", type=str, location='json', required=False)
    create_parser.add_argument("detailed_address", type=str, location='json', required=False)
    create_parser.add_argument("class_type", type=str, location='json', required=False)
    create_parser.add_argument("experience", type=str, location='json', required=False)
    create_parser.add_argument("other_information", type=str, location='json', required=False)
    create_parser.add_argument("latitude", type=float, location='json', required=False)
    create_parser.add_argument("longitude", type=float, location='json', required=False)

    create_verification_image_parser = get_auth_required_parser(api)
    create_verification_image_parser.add_argument("file", type=FileStorage, location="files", required=True)
    create_verification_image_parser.add_argument("description", type=str, location='form', required=True)
    create_verification_image_parser.add_argument("public", type=bool, location='form', required=True)

    certificate_parser = get_auth_required_parser(api)
    certificate_parser.add_argument("file", type=FileStorage, location="files", required=True)

    update_verification_image_parser = get_auth_required_parser(api)
    update_verification_image_parser.add_argument("file", type=FileStorage, location="files", required=True)
    update_verification_image_parser.add_argument("description", type=str, location='form', required=False)

    update_parser = get_auth_required_parser(api)
    update_parser.add_argument("career", type=str, location='json', required=False)
    update_parser.add_argument("tutor_description", type=str, location='json', required=False)
    update_parser.add_argument("subject", type=str, location='json', required=False)
    update_parser.add_argument("majors", type=str, location='json', required=False)
    update_parser.add_argument("degree", type=str, location='json', required=False)
    update_parser.add_argument("school", type=str, location='json', required=False)
    update_parser.add_argument("city_address", type=str, location='json', required=False)
    update_parser.add_argument("district_address", type=str, location='json', required=False)
    update_parser.add_argument("detailed_address", type=str, location='json', required=False)
    update_parser.add_argument("latitude", type=float, location='json', required=False)
    update_parser.add_argument("longitude", type=float, location='json', required=False)
    update_parser.add_argument("class_type", type=str, location='json', required=False)
    update_parser.add_argument("experience", type=str, location='json', required=False)
    update_parser.add_argument("other_information", type=str, location='json', required=False)

    filter_parser = get_auth_not_required_parser(api)
    filter_parser.add_argument("keyword", type=str, location='args', required=False)
    filter_parser.add_argument("user_id", type=int, location='args', required=False)
    filter_parser.add_argument("public_id", type=str, location='args', required=False)
    filter_parser.add_argument("career", type=str, location='args', required=False)
    filter_parser.add_argument("subject", type=str, location='args', required=False)
    filter_parser.add_argument("tutor_description", type=str, location='args', required=False)
    filter_parser.add_argument("majors", type=str, location='args', required=False)
    filter_parser.add_argument("degree", type=str, location='args', required=False)
    filter_parser.add_argument("school", type=str, location='args', required=False)
    filter_parser.add_argument("city_address", type=str, location='args', required=False)
    filter_parser.add_argument("district_address", type=str, location='args', required=False)
    filter_parser.add_argument("detailed_address", type=str, location='args', required=False)
    filter_parser.add_argument("class_type", type=str, location='args', required=False)
    filter_parser.add_argument("experience", type=str, location='args', required=False)
    filter_parser.add_argument("other_information", type=str, location='args', required=False)
    filter_parser.add_argument("status", type=str, location='args', required=False)
    filter_parser.add_argument("page", type=int, location="args", required=False, default=app.config['DEFAULT_PAGE'])
    filter_parser.add_argument("page_size", type=int, location="args", required=False,
                               default=app.config['DEFAULT_PAGE_SIZE'])
    """data"""
    image = api.inherit('image', {
        'id': fields.Integer(required=False, description='user email address'),
        'description': fields.String(required=False, description='user email address'),
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
    pagination_data = api.model('pagination', {
        'page': fields.Integer,
        'total': fields.Integer,
    })
    """response"""

    tutor_response = api.inherit('tutor_response', base, {
        'data': fields.Nested(tutor_data)
    })

    tutor_list_response = api.inherit('tutor_list_response', base, {
        'data': fields.List(fields.Nested(tutor_data)),
        'pagination': fields.Nested(pagination_data)
    })

    message_response = api.inherit('message_response', base, {
        'data': fields.String,
    })
