from datetime import datetime
from operator import or_

from sqlalchemy import desc

import app.util.response_message as response_message
from app import db
from app.model.class_model import Class
from app.model.rate_model import Rate
from app.model.user_model import User
from app.util.api_response import response_object


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


def create(args, user_id, author_id):
    author = User.query.get(author_id)
    if not author:
        return response_object(status=False, message=response_message.USER_NOT_FOUND), 404
    user = User.query.get(user_id)
    if not user:
        return response_object(status=False, message=response_message.USER_NOT_FOUND), 404
    star = args['star']
    content = args['content']
    classes = Class.query.filter(or_(Class.student_id == author_id, Class.teacher_id == author_id)).all()
    rate = Rate.query.filter(Rate.user_id == user_id, Rate.author_id == author_id).all()

    if len(classes) == 0:
        return response_object(status=False, message=response_message.NOT_STUDIED_OR_TAUGHT), 400

    if len(classes) > len(rate):
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
        user.number_of_rate = len(user.rates) + 1
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

    user.average_rating = total_rating / len(user.rates)
    user.number_of_rate = len(user.rates)
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
    user.number_of_rate = len(user.rates)
    db.session.commit()

    return response_object(), 200
