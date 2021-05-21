import uuid
from operator import or_

from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restx import Resource

from app import db
from app.dto.tutor_dto import TutorDto
from app.model.tutor_model import Tutor
from app.model.user_model import User
from app.util import response_message
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
    @api.response(404, 'Not found')
    @api.response(500, 'Internal server error')
    @api.expect(_create_request, validate=True)
    @api.marshal_with(_message_response, 201)
    @jwt_required()
    @tutor_required()
    def post(self):
        """Create tutor (Tạo gia sư)"""
        args = _create_request.parse_args()

        user = User.query.get(get_jwt_identity()['user_id'])
        if not user:
            return response_object(status=False, message=response_message.NOT_FOUND), 404
        if user.is_tutor:
            return response_object(status=False, message=response_message.ACCOUNT_IS_A_TUTOR_ALREADY), 400
        tutor = Tutor(
            public_id='GS' + str(uuid.uuid4())[:6].upper(),
            career=args['career'],
            tutor_description=args['tutor_description'],
            majors=args['majors'],
            degree=args['degree'],
            school=args['school'],
            address=args['address'],
            subject=args['subject'],
            class_type=args['class_type'],
            experience=args['experience'],
            other_information=args['other_information'],
        )
        db.session.add(tutor)
        db.session.flush()
        user.tutor_id = tutor.id
        user.is_tutor = True
        db.session.commit()
        return response_object(), 201

    # ok
    @api.doc('filter tutor')
    @api.expect(_filter_request, validate=True)
    @api.response(401, 'Unauthorized')
    @api.response(403, 'Forbidden')
    @api.response(404, 'Not found')
    @api.response(500, 'Internal server error')
    @api.marshal_with(_filter_response, 200)
    def get(self):
        """Filter tutors (Lọc các gia sư)"""
        args = _filter_request.parse_args()
        page = args['page']
        page_size = args['page_size']

        tutors = Tutor.query.filter(
            or_(Tutor.user.has(User.id == args['user_id']), args['user_id'] is None),
            or_(Tutor.public_id == args['public_id'], args['public_id'] is None),
            or_(Tutor.career.like("%{}%".format(args['career'])), args['career'] is None),
            or_(Tutor.tutor_description.like("%{}%".format(args['tutor_description'])),
                args['tutor_description'] is None),
            or_(Tutor.majors.like("%{}%".format(args['majors'])), args['majors'] is None),
            or_(Tutor.degree.like("%{}%".format(args['degree'])), args['degree'] is None),
            or_(Tutor.school.like("%{}%".format(args['school'])), args['school'] is None),
            or_(Tutor.address.like("%{}%".format(args['address'])), args['address'] is None),
            or_(Tutor.class_type.like("%{}%".format(args['class_type'])), args['class_type'] is None),
            or_(Tutor.experience.like("%{}%".format(args['experience'])), args['experience'] is None),
            or_(Tutor.other_information.like("%{}%".format(args['other_information'])),
                args['other_information'] is None),
            Tutor.is_active == True
        ).paginate(page, page_size, error_out=False)

        return response_object(data=[tutor.to_json() for tutor in tutors.items],
                               pagination={'total': tutors.total, 'page': tutors.page}), 200


@api.route('/<tutor_id>')
class TutorController(Resource):
    # tạm ok
    # chưa jwt
    @api.doc('get tutor by id')
    @api.response(401, 'Unauthorized')
    @api.response(403, 'Forbidden')
    @api.response(404, 'Not found')
    @api.response(500, 'Internal server error')
    @api.expect(get_auth_not_required_parser(api), validate=True)
    @api.marshal_with(_tutor_response, 200)
    def get(self, tutor_id):
        """Get a tutor by id (Get 1 gia sư)"""
        tutor = Tutor.query.filter(Tutor.id == tutor_id, Tutor.is_active).first()

        return response_object(data=tutor.to_json()), 200

    # cũng ok
    # chưa jwt
    @api.doc('update tutor')
    @api.response(401, 'Unauthorized')
    @api.response(403, 'Forbidden')
    @api.response(404, 'Not found')
    @api.response(500, 'Internal server error')
    @api.expect(_update_request, validate=True)
    @api.marshal_with(_message_response, 200)
    def put(self):
        """Update tutor (Cập nhật thông tin gia sư)"""
        args = _update_request.parse_args()
        tutor = Tutor.query.get(args['id'])
        if not tutor:
            return response_object(status=False, message=response_message.NOT_FOUND), 404

        tutor.career = args['career'] if args['career'] else tutor.career
        tutor.tutor_description = args['tutor_description'] if args['tutor_description'] else tutor.tutor_description
        tutor.majors = args['majors'] if args['majors'] else tutor.majors
        tutor.degree = args['degree'] if args['degree'] else tutor.degree
        tutor.school = args['school'] if args['school'] else tutor.school
        tutor.address = args['address'] if args['address'] else tutor.address
        tutor.class_type = args['class_type'] if args['class_type'] else tutor.class_type
        tutor.experience = args['experience'] if args['experience'] else tutor.experience
        tutor.other_information = args['other_information'] if args['other_information'] else tutor.other_information

        db.session.commit()

        return response_object()

    # chưa jwt
    @api.doc('delete tutor')
    @api.response(401, 'Unauthorized')
    @api.response(403, 'Forbidden')
    @api.response(404, 'Not found')
    @api.response(500, 'Internal server error')
    @api.expect(get_auth_required_parser(api), validate=True)
    @api.marshal_with(_message_response, 200)
    def delete(self, tutor_id):
        """Delete a tutor (Xóa 1 gia sư)"""
        tutor = Tutor.query.get(tutor_id)
        if not tutor:
            return response_object(status=False, message=response_message.NOT_FOUND), 404

        tutor.is_active = False
        db.session.commit()

        return response_object(), 200
