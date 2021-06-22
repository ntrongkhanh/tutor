import uuid
from datetime import datetime
from operator import or_

from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restx import Resource
from sqlalchemy import desc

from app import db, es
from app.dto.tutor_dto import TutorDto
from app.model.image_model import Image
from app.model.model_enum import TutorStatus
from app.model.tutor_model import Tutor
from app.model.user_model import User
from app.util import response_message, elasticsearch_index
from app.util.api_response import response_object
from app.util.auth_parser_util import get_auth_required_parser, get_auth_not_required_parser
from app.util.jwt_util import tutor_required

api = TutorDto.api

_message_response = TutorDto.message_response

_create_request = TutorDto.create_parser

_update_request = TutorDto.update_parser

_filter_request = TutorDto.filter_parser
_filter_response = TutorDto.tutor_list_response

_tutor_response = TutorDto.tutor_response


@api.route('')
class TutorListController(Resource):
    # tạm ok
    # truyền jwt get user id
    @api.doc('create tutor')
    @api.expect(_create_request, validate=True)
    # @api.marshal_with(_message_response, 201)
    @jwt_required()
    def post(self):
        """Create tutor (Tạo gia sư)"""
        args = _create_request.parse_args()
        user_id = get_jwt_identity()['user_id']
        return create(args, user_id)

    # ok
    @api.doc('filter tutor')
    @api.expect(_filter_request, validate=True)
    # @api.marshal_with(_filter_response, 200)
    def get(self):
        """Filter tutors (Lọc các gia sư)"""
        args = _filter_request.parse_args()
        return filter_tutor(args)

    # cũng ok
    # chưa jwt
    @api.doc('update tutor')
    @api.expect(_update_request, validate=True)
    # @api.marshal_with(_message_response, 200)
    @jwt_required()
    @tutor_required()
    def put(self):
        """Update tutor (Cập nhật thông tin gia sư)"""
        args = _update_request.parse_args()
        user_id = get_jwt_identity()['user_id']

        return update(args, user_id)


def create(args, user_id):
    user = User.query.get(user_id)
    if not user:
        return response_object(status=False, message=response_message.USER_NOT_FOUND), 404
    if user.is_tutor:
        return response_object(status=False, message=response_message.ACCOUNT_IS_A_TUTOR_ALREADY), 400
    tutor = Tutor(
        public_id='GS' + str(uuid.uuid4())[:6].upper(),
        career=args['career'],
        tutor_description=args['tutor_description'],
        majors=args['majors'],
        degree=args['degree'],
        school=args['school'],
        city_address=args['city_address'],
        district_address=args['district_address'],
        detailed_address=args['detailed_address'],
        subject=args['subject'],
        class_type=args['class_type'],
        experience=args['experience'],
        other_information=args['other_information']
    )
    db.session.add(tutor)
    db.session.flush()
    user.tutor_id = tutor.id
    user.is_tutor = True
    db.session.commit()

    body = {
        'id': user.id,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'is_tutor': user.is_tutor,
        'public_id': user.tutor.public_id,
        'career': tutor.career,
        'tutor_description': tutor.tutor_description,
        'majors': tutor.majors,
        'degree': tutor.degree,
        'school': tutor.school,
        'city_address': tutor.city_address,
        'district_address': tutor.district_address,
        'detailed_address': tutor.detailed_address,
        'latitude': tutor.latitude,
        'longitude': tutor.longitude,
        'subject': tutor.subject,
        'class_type': tutor.class_type
    }
    es.index(index=elasticsearch_index.TUTOR, id=body['id'], body=body)

    return response_object(), 201


def filter_tutor(args):
    page = args['page']
    page_size = args['page_size']
    keyword = args['keyword']
    id_list = []
    if keyword and keyword != '':
        body = {
            "size": 1000,
            "query": {
                "multi_match": {
                    "query": keyword,
                    "fields": ["id", "first_name", "last_name", "public_id", "career", "tutor_description", "majors",
                               "degree", "school", "city_address", "district_address", "detailed_address", "latitude",
                               "longitude", "subject", "class_type"]
                },
            },
        }

        res = es.search(index=elasticsearch_index.TUTOR, body=body)

        res_list = res['hits']['hits']

        id_list = [re['_id'] for re in res_list]

    users = User.query.filter(
        User.id.in_(id_list) if len(id_list) > 0 else True,
        User.is_tutor,
        or_(User.id == args['user_id'], args['user_id'] is None),
        or_(User.tutor.has(Tutor.public_id.like("%{}%".format(args['public_id']))), args['public_id'] is None),
        or_(User.tutor.has(Tutor.subject.like("%{}%".format(args['subject']))), args['subject'] is None),
        or_(User.tutor.has(Tutor.career.like("%{}%".format(args['career']))), args['career'] is None),
        or_(User.tutor.has(Tutor.majors.like("%{}%".format(args['majors']))), args['majors'] is None),
        or_(User.tutor.has(Tutor.degree.like("%{}%".format(args['degree']))), args['degree'] is None),
        or_(User.tutor.has(Tutor.city_address.like("%{}%".format(args['city_address']))), args['city_address'] is None),
        or_(User.tutor.has(Tutor.district_address.like("%{}%".format(args['district_address']))),
            args['district_address'] is None),
        or_(User.tutor.has(Tutor.detailed_address.like("%{}%".format(args['detailed_address']))),
            args['detailed_address'] is None),
        or_(User.tutor.has(Tutor.class_type.like("%{}%".format(args['class_type']))), args['class_type'] is None),
        or_(User.tutor.has(Tutor.experience.like("%{}%".format(args['experience']))), args['experience'] is None),
        User.tutor.has(Tutor.status == TutorStatus.APPROVED),
        User.is_active
    ).paginate(page, page_size, error_out=False)

    # tutors = Tutor.query.filter(
    #
    #     (Tutor.status == args['status'] if identity and get_jwt_identity()['is_admin']
    #      else Tutor.status == TutorStatus.APPROVED),
    #     Tutor.is_active
    # ).paginate(page, page_size, error_out=False)

    return response_object(data=[user.to_json_tutor() for user in users.items],
                           pagination={'total': users.total, 'page': users.page}), 200


def update(args, user_id):
    user = User.query.get(user_id)

    if not user:
        return response_object(status=False, message=response_message.NOT_FOUND_404), 404
    tutor = Tutor.query.get(user.tutor_id)
    if not tutor:
        return response_object(status=False, message=response_message.NOT_FOUND_404), 404

    tutor.career = args['career'] if args['career'] else tutor.career
    tutor.tutor_description = args['tutor_description'] if args['tutor_description'] else tutor.tutor_description
    tutor.majors = args['majors'] if args['majors'] else tutor.majors
    tutor.degree = args['degree'] if args['degree'] else tutor.degree
    tutor.subject = args['subject'] if args['subject'] else tutor.subject
    tutor.school = args['school'] if args['school'] else tutor.school
    tutor.city_address = args['city_address'] if args['city_address'] else tutor.city_address
    tutor.district_address = args['district_address'] if args['district_address'] else tutor.district_address
    tutor.detailed_address = args['detailed_address'] if args['detailed_address'] else tutor.detailed_address
    tutor.class_type = args['class_type'] if args['class_type'] else tutor.class_type
    tutor.experience = args['experience'] if args['experience'] else tutor.experience
    tutor.other_information = args['other_information'] if args['other_information'] else tutor.other_information
    tutor.latitude = args['latitude'] if args['latitude'] else tutor.latitude
    tutor.longitude = args['longitude'] if args['longitude'] else tutor.longitude
    tutor.updated_date = datetime.now()

    db.session.commit()

    body = {
        'id': user.id,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'is_tutor': user.is_tutor,
        'public_id': tutor.public_id,
        'career': tutor.career,
        'tutor_description': tutor.tutor_description,
        'majors': tutor.majors,
        'degree': tutor.degree,
        'school': tutor.school,
        'city_address': tutor.city_address,
        'district_address': tutor.district_address,
        'detailed_address': tutor.detailed_address,
        'latitude': tutor.latitude,
        'longitude': tutor.longitude,
        'subject': tutor.subject,
        'class_type': tutor.class_type
    }
    es.index(index=elasticsearch_index.TUTOR, id=body['id'], body=body)

    return response_object(), 200


_create_verification_image_parser = TutorDto.create_verification_image_parser


@api.route('/verification-image')
class VerificationImageListController(Resource):
    @api.doc('verification image')
    @api.expect(_create_verification_image_parser, validate=True)
    # @api.marshal_with(_message_response, 201)
    @jwt_required()
    def post(self):
        """upload verification image"""
        user_id = get_jwt_identity()['user_id']
        args = _create_verification_image_parser.parse_args()
        return upload_verification_image(args, user_id)


def upload_verification_image(args, user_id):
    user = User.query.get(user_id)
    if not user:
        return response_object(status=False, message=response_message.USER_NOT_FOUND), 404
    tutor = Tutor.query.get(user.tutor_id)
    if not tutor:
        return response_object(status=False, message=response_message.TUTOR_NOT_FOUND), 404

    file = args['file'].read()
    description = request.form['description']
    public = request.form['public']

    image = Image(data=file, description=description, tutor_id=tutor.id,
                  is_public=True if public == 'true' else False)
    db.session.add(image)
    db.session.commit()

    return response_object(), 201


_update_verification_image_parser = TutorDto.update_verification_image_parser


@api.route('/verification-image/<image_id>')
class VerificationImageController(Resource):
    @api.doc('update verification image')
    @api.expect(_update_verification_image_parser, validate=True)
    # @api.marshal_with(_message_response, 201)
    @jwt_required()
    def put(self, image_id):
        user_id = get_jwt_identity()['user_id']
        args = _update_verification_image_parser.parse_args()
        return update_verification_image(args, image_id, user_id)

    @api.doc('delete verification image')
    @api.expect(get_auth_required_parser(api), validate=True)
    # @api.marshal_with(_message_response, 201)
    @jwt_required()
    def delete(self, image_id):
        user_id = get_jwt_identity()['user_id']
        return delete_verification_image(image_id, user_id)


def update_verification_image(args, image_id, user_id):
    user = User.query.get(user_id)
    if not user:
        return response_object(status=False, message=response_message.USER_NOT_FOUND), 404
    tutor = Tutor.query.get(user.tutor_id)
    if not tutor:
        return response_object(status=False, message=response_message.TUTOR_NOT_FOUND), 404

    image = Image.query.get(image_id)
    if not image:
        return response_object(status=False, message=response_message.NOT_FOUND_404), 404
    if image.tutor_id != user.tutor_id:
        return response_object(status=False, message=response_message.UNAUTHORIZED_401), 401

    file = args['file'].read()

    image.description = args['description'] if args['description'] else image.description
    image.data = file
    image.updated_date = datetime.now()

    db.session.commit()

    return response_object(), 200


def delete_verification_image(image_id, user_id):
    user = User.query.get(user_id)
    if not user:
        return response_object(status=False, message=response_message.USER_NOT_FOUND), 404
    tutor = Tutor.query.get(user.tutor_id)
    if not tutor:
        return response_object(status=False, message=response_message.TUTOR_NOT_FOUND), 404

    image = Image.query.get(image_id)
    if not image:
        return response_object(status=False, message=response_message.NOT_FOUND_404), 404
    if image.tutor_id != user.tutor_id:
        return response_object(status=False, message=response_message.UNAUTHORIZED_401), 401

    db.session.delete(image)
    db.session.commit()

    return response_object(), 200


@api.route('/<tutor_id>')
class TutorController(Resource):
    # tạm ok
    # chưa jwt
    @api.doc('get tutor by id')
    @api.expect(get_auth_not_required_parser(api), validate=True)
    # @api.marshal_with(_tutor_response, 200)
    def get(self, tutor_id):
        """Get a tutor by id (Get 1 gia sư)"""
        return get_by_id(tutor_id)

    # chưa jwt
    # @api.doc('delete tutor')
    # @api.expect(get_auth_required_parser(api), validate=True)
    # #@api.marshal_with(_message_response, 200)
    # def delete(self, tutor_id):
    #     """Delete a tutor (Xóa 1 gia sư)"""
    #     tutor = Tutor.query.get(tutor_id)
    #     if not tutor:
    #         return response_object(status=False, message=response_message.NOT_FOUND_404), 404
    #
    #     tutor.is_active = False
    #     db.session.commit()
    #
    #     return response_object(), 200


def get_by_id(tutor_id):
    tutor = Tutor.query.filter(Tutor.id == tutor_id, Tutor.is_active).first()
    if not tutor:
        return response_object(status=False, message=response_message.TUTOR_NOT_FOUND), 404

    return response_object(data=tutor.to_json()), 200


@api.route('/profile')
class Profile(Resource):
    @api.doc('profile')
    @api.expect(get_auth_required_parser(api), validate=True)
    # @api.marshal_with(_tutor_response, 200)
    @jwt_required()
    @tutor_required()
    def get(self):
        user_id = get_jwt_identity()['user_id']
        return get_profile(user_id)


@api.route('/best')
class BestTutorListController(Resource):
    @api.doc('best list')
    def get(self):
        return get_best_list()


def get_best_list():
    users = User.query.filter(User.is_tutor).order_by(desc(User.average_rating)).limit(4).all()

    return response_object(data=[user.to_json() for user in users]), 200


def get_profile(user_id):
    # tutor = Tutor.query.filter(Tutor.user.has(User.id == user_id)).first()
    tutor = Tutor.query.filter(Tutor.user.has(User.id == user_id), Tutor.is_active).first()
    if not tutor:
        return response_object(status=False, message=response_message.NOT_FOUND_404), 404
    return response_object(data=tutor.to_json()), 200
