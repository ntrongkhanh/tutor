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


@api.route('/create')
class create(Resource):
    @api.doc('create tutor')
    @api.expect(_create_parser, validate=True)
    def post(self):
        args = _create_parser.parse_args()
        user = User.query.get(args['user_id'])
        if not user:
            return response_object(status=False, message=response_message.NOT_FOUND), 404
        tutor = Tutor(
            public_id=uuid.uuid4(),
            career=args['career'],
            tutor_description=args['tutor_description'],
            majors=args['majors'],
            degree=args['degree'],
            school=args['school'],
            address=args['address'],
            class_type=args['class_type'],
            experience=args['experience'],
            other_information=args['other_information'],
        )
        db.session.add(tutor)
        user.tutor_id = tutor.id
        db.session.commit()
        return response_object(data=tutor.to_json()), 200


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


@api.route('/update')
class update(Resource):
    @api.doc('update tutor')
    @api.expect(_update_parser, validate=True)
    def put(self):
        args = _update_parser.parse_args()
        tutor = Tutor.query.get(args['id'])
        if not tutor:
            return response_object(status=False, message=response_message.NOT_FOUND), 404

        tutor.career = args['career']
        tutor.tutor_description = args['tutor_description']
        tutor.majors = args['majors']
        tutor.degree = args['degree']
        tutor.school = args['school']
        tutor.address = args['address']
        tutor.class_type = args['class_type']
        tutor.experience = args['experience']
        tutor.other_information = args['other_information']

        db.session.commit()

        return response_object(data=tutor.to_json()), 200


@api.route('/delete/<id>')
class delete(Resource):
    @api.doc('delete tutor')
    def delete(self, id):
        tutor = Tutor.query.get(id)
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


@api.route('/')
class filter(Resource):
    @api.doc('filter tutor')
    @api.expect(_filter_parser)
    def get(self):
        args = _filter_parser.parse_args()

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
        )

        return response_object(data=[tutor.to_json() for tutor in tutors]), 200


@api.route('/<id>')
class get(Resource):
    @api.doc('get tutor by id')
    def get(self, id):
        tutor = Tutor.query.filter(Tutor.id == id, Tutor.is_active).first()

        return response_object(data=tutor.to_json()), 200
