import uuid
from operator import or_

from flask_restx import Resource

from app import db
from app.dto.tutor_dto import TutorDto
from app.model.tutor_model import Tutor
from app.model.user_model import User
from app.util import response_message
from app.util.api_response import response_object

api = TutorDto.api

_message_response = TutorDto.message_response

_create_parser = api.parser()
_create_parser.add_argument("user_id", type=int, location='json', required=True)
_create_parser.add_argument("career", type=str, location='json', required=False)
_create_parser.add_argument("tutor_description", type=str, location='json', required=False)
_create_parser.add_argument("majors", type=str, location='json', required=False)
_create_parser.add_argument("degree", type=str, location='json', required=False)
_create_parser.add_argument("school", type=str, location='json', required=False)
_create_parser.add_argument("address", type=str, location='json', required=False)
_create_parser.add_argument("class_type", type=str, location='json', required=False)
_create_parser.add_argument("experience", type=str, location='json', required=False)
_create_parser.add_argument("other_information", type=str, location='json', required=False)


# sai
@api.route('/create')
class Create(Resource):
    @api.doc('create tutor')
    @api.expect(_create_parser, validate=True)
    @api.response(404, 'Not found')
    @api.response(500, 'Internal server error')
    @api.marshal_with(_message_response, 201)
    def post(self):
        """Create tutor (Tạo gia sư)"""
        args = _create_parser.parse_args()
        user = User.query.get(args['user_id'])
        if not user:
            return response_object(status=False, message=response_message.NOT_FOUND), 404
        tutor = Tutor(
            public_id='G' + str(uuid.uuid4())[:8].upper(),
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
        user.tutor_id = tutor.id
        db.session.commit()
        return response_object(), 201


_update_parser = api.parser()
_update_parser.add_argument("id", type=int, location='json', required=True)
_update_parser.add_argument("career", type=str, location='json', required=False)
_update_parser.add_argument("tutor_description", type=str, location='json', required=False)
_update_parser.add_argument("majors", type=str, location='json', required=False)
_update_parser.add_argument("degree", type=str, location='json', required=False)
_update_parser.add_argument("school", type=str, location='json', required=False)
_update_parser.add_argument("address", type=str, location='json', required=False)
_update_parser.add_argument("class_type", type=str, location='json', required=False)
_update_parser.add_argument("experience", type=str, location='json', required=False)
_update_parser.add_argument("other_information", type=str, location='json', required=False)


# cũng ok
@api.route('/update')
class Update(Resource):
    @api.doc('update tutor')
    @api.expect(_update_parser, validate=True)
    @api.response(401, 'Unauthorized')
    @api.response(403, 'Forbidden')
    @api.response(404, 'Not found')
    @api.response(500, 'Internal server error')
    @api.marshal_with(_message_response, 200)
    def put(self):
        """Update tutor (Cập nhật thông tin gia sư)"""
        args = _update_parser.parse_args()
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


# ok
# chưa jwt
@api.route('/delete/<tutor_id>')
class Delete(Resource):
    @api.doc('delete tutor')
    @api.response(401, 'Unauthorized')
    @api.response(403, 'Forbidden')
    @api.response(404, 'Not found')
    @api.response(500, 'Internal server error')
    @api.marshal_with(_message_response, 200)
    def delete(self, tutor_id):
        """Delete a tutor (Xóa 1 gia sư)"""
        tutor = Tutor.query.get(tutor_id)
        if not tutor:
            return response_object(status=False, message=response_message.NOT_FOUND), 404

        tutor.is_active = False
        db.session.commit()

        return response_object(), 200


_filter_parser = api.parser()
_filter_parser.add_argument("user_id", type=int, location='args', required=False)
_filter_parser.add_argument("public_id", type=int, location='args', required=False)
_filter_parser.add_argument("career", type=str, location='args', required=False)
_filter_parser.add_argument("tutor_description", type=str, location='args', required=False)
_filter_parser.add_argument("majors", type=str, location='args', required=False)
_filter_parser.add_argument("degree", type=str, location='args', required=False)
_filter_parser.add_argument("school", type=str, location='args', required=False)
_filter_parser.add_argument("address", type=str, location='args', required=False)
_filter_parser.add_argument("class_type", type=str, location='args', required=False)
_filter_parser.add_argument("experience", type=str, location='args', required=False)
_filter_parser.add_argument("other_information", type=str, location='args', required=False)

_filter_parser.add_argument("page", type=int, location="args", required=False, default=1)
_filter_parser.add_argument("page_size", type=int, location="args", required=False, default=10)
_filter_response = TutorDto.tutor_list_response


# ok
# sửa user như get by id
# public id quá dài
@api.route('/')
class Filter(Resource):
    @api.doc('filter tutor')
    @api.expect(_filter_parser, validate=True)
    @api.response(401, 'Unauthorized')
    @api.response(403, 'Forbidden')
    @api.response(404, 'Not found')
    @api.response(500, 'Internal server error')
    @api.marshal_with(_filter_response, 200)
    def get(self):
        """Filter tutors (Lọc các gia sư)"""
        args = _filter_parser.parse_args()
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


_tutor_response = TutorDto.tutor_response


# chưa  hiện đc user
# public id quá dài
@api.route('/<tutor_id>')
class Get(Resource):
    @api.doc('get tutor by id')
    @api.response(401, 'Unauthorized')
    @api.response(403, 'Forbidden')
    @api.response(404, 'Not found')
    @api.response(500, 'Internal server error')
    @api.marshal_with(_tutor_response, 200)
    def get(self, tutor_id):
        """Get a tutor by id (Get 1 gia sư)"""
        tutor = Tutor.query.filter(Tutor.id == tutor_id, Tutor.is_active).first()

        return response_object(data=tutor.to_json()), 200
