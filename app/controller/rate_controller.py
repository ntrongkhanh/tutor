from datetime import datetime

from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restx import Resource
from sqlalchemy import desc

import app.util.response_message as response_message
from app import db
from app.dto.rate_dto import RateDto
from app.model.rate_model import Rate
from app.model.user_model import User
from app.util.api_response import response_object
from app.util.auth_parser_util import get_auth_required_parser

api = RateDto.api

_rate_request = RateDto.rate_request
_filter_request = RateDto.filter_request
_message_response = RateDto.message_response


@api.route('')
class RateListController(Resource):
    @api.doc('get rated list')
    @api.expect(_filter_request, validate=True)
    @jwt_required()
    def get(self):
        """filter danh sách đánh giá của người khác cho mình"""
        args = _filter_request.parse_args()
        user_id = get_jwt_identity()['user_id']
        return filter_rate_list_for_user(args, user_id)


def filter_rate_list_for_user(args, user_id):
    user = User.query.get(user_id)
    if not user:
        return response_object(status=False, message=response_message.USER_NOT_FOUND), 404
    page = args['page']
    page_size = args['page_size']
    rates = Rate.query.filter(Rate.user_id == user_id) \
        .order_by(desc(Rate.updated_date)) \
        .paginate(page, page_size, error_out=False)

    return response_object(data=[rate.to_json() for rate in rates.items],
                           pagination={'total': rates.total, 'page': rates.page}), 200


@api.route('/<user_id>')
class CreateRateController(Resource):
    @api.doc('rate user')
    @api.expect(_rate_request, validate=True)
    # @api.marshal_with(_message_response, 201)
    @jwt_required()
    def post(self, user_id):
        """đánh giá"""
        args = _rate_request.parse_args()
        author_id = get_jwt_identity()['user_id']
        return create(args, user_id, author_id)

    @api.doc('filter rate')
    @api.expect(_filter_request, validate=True)
    def get(self, user_id):
        """filter danh sách đánh giá"""
        args = _filter_request.parse_args()
        return filter_rate(args, user_id)


@api.route('/get')
class RatedListController(Resource):
    @api.doc('get rate list what rated')
    @api.expect(_filter_request, validate=True)
    @jwt_required()
    def get(self):
        """filter danh sách các đánh giá mà mình đã đánh giá"""
        args = _filter_request.parse_args()
        author_id = get_jwt_identity()['user_id']
        return get_rated_list(args, author_id)


def get_rated_list(args, author_id):
    author = User.query.get(author_id)
    if not author:
        return response_object(status=False, message=response_message.USER_NOT_FOUND), 404
    page = args['page']
    page_size = args['page_size']
    rates = Rate.query.filter(Rate.author_id == author_id) \
        .order_by(desc(Rate.updated_date)) \
        .paginate(page, page_size, error_out=False)

    return response_object(data=[rate.to_json() for rate in rates.items],
                           pagination={'total': rates.total, 'page': rates.page}), 200


def filter_rate(args, user_id):
    user = User.query.get(user_id)
    if not user:
        return response_object(status=False, message=response_message.USER_NOT_FOUND), 404
    page = args['page']
    page_size = args['page_size']
    rates = Rate.query.filter(Rate.user_id == user_id) \
        .order_by(desc(Rate.updated_date)) \
        .paginate(page, page_size, error_out=False)

    return response_object(data=[rate.to_json() for rate in rates.items],
                           pagination={'total': rates.total, 'page': rates.page}), 200


@api.route('/<rate_id>')
class RateController(Resource):
    @api.doc('update rate')
    @api.expect(_rate_request, validate=True)
    # @api.marshal_with(_message_response, 200)
    @jwt_required()
    def put(self, rate_id):
        """update đánh giá"""
        args = _rate_request.parse_args()
        author_id = get_jwt_identity()['user_id']
        return update(args, rate_id, author_id)

    @api.doc('delete rate')
    @api.expect(get_auth_required_parser(api), validate=True)
    # @api.marshal_with(_message_response, 200)
    @jwt_required()
    def delete(self, rate_id):
        """xóa đánh giá"""
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
    rate = Rate.query.filter(Rate.user_id == user_id, Rate.author_id == author_id).first()
    if not rate:
        rate = Rate(
            star=star,
            content=content,
            user_id=user_id,
            author_id=author_id
        )
        total_rating = 0
        for temp_rate in user.rates:
            total_rating += temp_rate.star
        user.average_rating = (total_rating + star) / (len(user.rates) + 1)
        db.session.add(rate)
    else:
        return response_object(status=False, message=response_message.CONFLICT_409), 409

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
    for temp_rate in user.rates:
        total_rating += temp_rate.star
    print(total_rating)
    print(len(user.rates))
    print(str(rate.star - old_star))
    user.average_rating = total_rating / len(user.rates)

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
    db.session.delete(rate)
    user = User.query.get(rate.user_id)
    total_rating = 0
    for temp_rate in user.rates:
        total_rating += temp_rate.star
    if len(user.rates) == 0:
        user.average_rating = 0.0
    else:
        user.average_rating = total_rating / len(user.rates)

    db.session.commit()

    return response_object(), 200
