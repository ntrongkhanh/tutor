import uuid
from datetime import datetime
from operator import or_

from flask import request
from sqlalchemy import desc

from app import db, es
from app.model.image_model import Image
from app.model.model_enum import TutorStatus
from app.model.tutor_model import Tutor
from app.model.user_model import User
from app.util import response_message, elasticsearch_index
from app.util.api_response import response_object


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
        latitude=args['latitude'],
        longitude=args['longitude'],
        other_information=args['other_information']
    )
    db.session.add(tutor)
    db.session.flush()
    user.tutor_id = tutor.id
    user.is_tutor = True
    db.session.commit()
    if es.ping():
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
    if keyword and keyword != '' and es.ping():
        body = {
            "size": 1000,
            "query": {
                "multi_match": {
                    "query": keyword,
                    "fields": ["first_name", "last_name", "public_id", "career",
                               "city_address", "district_address", "detailed_address",
                               "subject", "class_type"]
                },
            },
        }

        res = es.search(index=elasticsearch_index.TUTOR, body=body)

        res_list = res['hits']['hits']

        id_list = [re['_id'] for re in res_list]
    if keyword and keyword != '':
        users = User.query.filter(
            User.id.in_(id_list) if len(id_list) > 0 else False,
            User.is_tutor,
            or_(User.id == args['user_id'], args['user_id'] is None),
            or_(User.tutor.has(Tutor.public_id.like("%{}%".format(args['public_id']))), args['public_id'] is None),
            or_(User.tutor.has(Tutor.subject.like("%{}%".format(args['subject']))), args['subject'] is None),
            or_(User.tutor.has(Tutor.career.like("%{}%".format(args['career']))), args['career'] is None),
            or_(User.tutor.has(Tutor.majors.like("%{}%".format(args['majors']))), args['majors'] is None),
            or_(User.tutor.has(Tutor.degree.like("%{}%".format(args['degree']))), args['degree'] is None),
            or_(User.tutor.has(Tutor.city_address.like("%{}%".format(args['city_address']))),
                args['city_address'] is None),
            or_(User.tutor.has(Tutor.district_address.like("%{}%".format(args['district_address']))),
                args['district_address'] is None),
            or_(User.tutor.has(Tutor.detailed_address.like("%{}%".format(args['detailed_address']))),
                args['detailed_address'] is None),
            or_(User.tutor.has(Tutor.class_type.like("%{}%".format(args['class_type']))), args['class_type'] is None),
            or_(User.tutor.has(Tutor.experience.like("%{}%".format(args['experience']))), args['experience'] is None),
            User.tutor.has(Tutor.status == TutorStatus.APPROVED),
            User.is_active
        ).paginate(page, page_size, error_out=False)
    else:
        users = User.query.filter(
            User.is_tutor,
            or_(User.id == args['user_id'], args['user_id'] is None),
            or_(User.tutor.has(Tutor.public_id.like("%{}%".format(args['public_id']))), args['public_id'] is None),
            or_(User.tutor.has(Tutor.subject.like("%{}%".format(args['subject']))), args['subject'] is None),
            or_(User.tutor.has(Tutor.career.like("%{}%".format(args['career']))), args['career'] is None),
            or_(User.tutor.has(Tutor.majors.like("%{}%".format(args['majors']))), args['majors'] is None),
            or_(User.tutor.has(Tutor.degree.like("%{}%".format(args['degree']))), args['degree'] is None),
            or_(User.tutor.has(Tutor.city_address.like("%{}%".format(args['city_address']))),
                args['city_address'] is None),
            or_(User.tutor.has(Tutor.district_address.like("%{}%".format(args['district_address']))),
                args['district_address'] is None),
            or_(User.tutor.has(Tutor.detailed_address.like("%{}%".format(args['detailed_address']))),
                args['detailed_address'] is None),
            or_(User.tutor.has(Tutor.class_type.like("%{}%".format(args['class_type']))), args['class_type'] is None),
            or_(User.tutor.has(Tutor.experience.like("%{}%".format(args['experience']))), args['experience'] is None),
            User.tutor.has(Tutor.status == TutorStatus.APPROVED),
            User.is_active
        ).order_by(User.average_rating.desc(), User.number_of_rate.desc()) \
            .paginate(page, page_size, error_out=False)
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
    if es.ping():
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


def certificate(file, user_id):
    user = User.query.get(user_id)
    if not user:
        return response_object(status=False, message=response_message.USER_NOT_FOUND), 404
    tutor = Tutor.query.get(user.tutor_id)
    if not tutor:
        return response_object(status=False, message=response_message.TUTOR_NOT_FOUND), 404

    data = file.read()

    image = Image(data=data,
                  description='Bằng cấp, chứng chỉ',
                  tutor_id=tutor.id,
                  is_public=True)
    db.session.add(image)
    db.session.commit()

    return response_object(), 201


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


def get_by_id(tutor_id):
    tutor = Tutor.query.filter(Tutor.id == tutor_id, Tutor.is_active).first()
    if not tutor:
        return response_object(status=False, message=response_message.TUTOR_NOT_FOUND), 404

    return response_object(data=tutor.to_json()), 200


def get_best_list():
    users = User.query.filter(User.is_tutor).order_by(desc(User.average_rating)).limit(4).all()

    return response_object(data=[user.to_json() for user in users]), 200


def get_profile(user_id):
    # tutor = Tutor.query.filter(Tutor.user.has(User.id == user_id)).first()
    tutor = Tutor.query.filter(Tutor.user.has(User.id == user_id), Tutor.is_active).first()
    if not tutor:
        return response_object(status=False, message=response_message.NOT_FOUND_404), 404
    return response_object(data=tutor.to_json()), 200
