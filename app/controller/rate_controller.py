from datetime import datetime

from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restx import Resource

import app.util.response_message as response_message
from app import db
from app.dto.rate_dto import RateDto
from app.model.rate_model import Rate
from app.model.user_model import User
from app.util.api_response import response_object
from app.util.auth_parser_util import get_auth_required_parser

api = RateDto.api

_rate_request = RateDto.rate_request
_message_response = RateDto.message_response


@api.route('/<user_id>')
class CreateRateController(Resource):
    @api.doc('rate user')
    @api.expect(_rate_request, validate=True)
    @api.marshal_with(_message_response, 201)
    @jwt_required()
    def post(self, user_id):
        args = _rate_request.parse_args()
        author_id = get_jwt_identity()['user_id']
        return create(args, user_id, author_id)


@api.route('/<rate_id>')
class RateController(Resource):
    @api.doc('update rate')
    @api.expect(_rate_request, validate=True)
    @api.marshal_with(_message_response, 200)
    @jwt_required()
    def put(self, rate_id):
        args = _rate_request.parse_args()
        author_id = get_jwt_identity()['user_id']
        return update(args, rate_id, author_id)

    @api.doc('delete rate')
    @api.expect(get_auth_required_parser(api), validate=True)
    @api.marshal_with(_message_response, 200)
    @jwt_required()
    def delete(self, rate_id):
        author_id = get_jwt_identity()['user_id']
        return delete(rate_id, author_id)


def create(args, user_id, author_id):
    author = User.query.get(author_id)
    if not author:
        return response_object(status=False, message=response_message.USER_NOT_FOUND), 404
    user = User.query.get(user_id)
    if not user:
        return response_object(status=False, message=response_message.USER_NOT_FOUND), 404
    star = args['star']
    content = args['content']
    rate = Rate(
        star=star,
        content=content,
        user_id=user_id,
        author_id=author_id
    )
    total_rating = 0
    for rate in user.rates:
        total_rating += rate.star
    user.average_rating = (total_rating + star) / (len(user.rates) + 1)
    db.session.add(rate)
    db.session.commit()
    return response_object(), 201


def update(args, rate_id, author_id):
    author = User.query.get(author_id)
    if not author:
        return response_object(status=False, message=response_message.USER_NOT_FOUND), 404
    rate = Rate.query.get(rate_id)
    if not rate:
        return response_object(status=False, message=response_message.NOT_FOUND_404), 404
    if rate.author_id != author_id:
        return response_object(status=False, message=response_message.UNAUTHORIZED_401), 401
    old_star = rate.star
    rate.star = args['star'] if args['star'] else rate.star
    rate.content = args['content'] if args['content'] else rate.content
    rate.updated_date = datetime.now()

    user = User.query.get(rate.user_id)
    total_rating = 0
    for rate in user.rates:
        total_rating += rate.star
    user.average_rating = (total_rating + rate.star - old_star) / len(user.rates)

    db.session.commit()
    return response_object(), 200


def delete(rate_id, author_id):
    author = User.query.get(author_id)
    if not author:
        return response_object(status=False, message=response_message.USER_NOT_FOUND), 404
    rate = Rate.query.get(rate_id)
    if not rate:
        return response_object(status=False, message=response_message.NOT_FOUND_404), 404
    if rate.author_id != author_id:
        return response_object(status=False, message=response_message.UNAUTHORIZED_401), 401

    user = User.query.get(rate.user_id)
    total_rating = 0
    for rate in user.rates:
        total_rating += rate.star
    user.average_rating = (total_rating - rate.star) / (len(user.rates) - 1)

    db.session.delete(rate)
    db.session.commit()

    return response_object(), 200
