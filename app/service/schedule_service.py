from datetime import datetime

from app import db
from app.model.post_model import Post
from app.model.schedule_model import Schedule
from app.model.user_model import User
from app.util import response_message
from app.util.api_response import response_object


def create(args, user_id):
    user = User.query.get(user_id)
    if not user:
        return response_object(status=False, message=response_message.USER_NOT_FOUND), 404
    post = Post.query.get(args['post_id'])
    if not post:
        return response_object(status=False, message=response_message.POST_NOT_FOUND), 404
    schedule = Schedule(day=args['day'],
                        start_time=args['start_time'],
                        end_time=args['end_time'],
                        post_id=args['post_id'])
    db.session.add(schedule)
    db.session.commit()
    return response_object(), 201


def get_by_id(schedule_id):
    schedule = Schedule.query.get(schedule_id)
    if not schedule:
        return response_object(status=False, message=response_message.SCHEDULE_NOT_FOUND), 404
    return response_object(data=schedule.to_json()), 200


def update(args, schedule_id, user_id):
    user = User.query.get(user_id)
    if not user:
        return response_object(status=False, message=response_message.USER_NOT_FOUND), 404
    schedule = Schedule.query.get(schedule_id)
    if not schedule:
        return response_object(status=False, message=response_message.SCHEDULE_NOT_FOUND), 404

    if schedule.post.user_id != user_id:
        return response_object(status=False, message=response_message.UNAUTHORIZED_401), 401

    schedule.updated_date = datetime.now()
    schedule.day = args['day'] if args['day'] else schedule.day
    schedule.start_time = args['start_time'] if args['start_time'] else schedule.start_time
    schedule.end_time = args['end_time'] if args['end_time'] else schedule.end_time

    db.session.commit()
    return response_object(), 200


def delete(schedule_id, user_id):
    user = User.query.get(user_id)
    if not user:
        return response_object(status=False, message=response_message.USER_NOT_FOUND), 404
    schedule = Schedule.query.get(schedule_id)
    if not schedule:
        return response_object(status=False, message=response_message.SCHEDULE_NOT_FOUND), 404

    if schedule.post.user_id != user_id:
        return response_object(status=False, message=response_message.UNAUTHORIZED_401), 401
    db.session.delete(schedule)
    db.session.commit()
    return response_object(), 200
