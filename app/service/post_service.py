import uuid
from datetime import datetime
from operator import or_, and_

from sqlalchemy import desc

import app.util.response_message as response_message
from app import db, es
from app.model.class_model import Class
from app.model.model_enum import PostStatus, RegistrationStatus
from app.model.post_model import Post
from app.model.rate_model import Rate
from app.model.registration_model import Registration
from app.model.schedule_model import Schedule
from app.model.user_model import User
from app.util import elasticsearch_index
from app.util.api_response import response_object


def create_tutor_post(args, user_id):
    user = User.query.get(user_id)
    if not user:
        return response_object(status=False, message=response_message.UNAUTHORIZED_401), 401

    post = Post(
        public_id='BD' + str(uuid.uuid4())[:6].upper(),
        is_tutor=True,
        title=args['title'],
        description=args['description'],
        city_address=args['city_address'],
        district_address=args['district_address'],
        detailed_address=args['detailed_address'],
        latitude=args['latitude'],
        longitude=args['longitude'],
        subject=args['subject'],
        class_type=args['class_type'],
        other_information=args['other_information'],
        fee=args['fee'],
        # schedule=args['schedule'],
        number_of_sessions=args['number_of_sessions'],
        require=args['require'],
        contact=args['contact'],
        form_of_teaching=args['form_of_teaching'],
        user_id=user.id
    )
    db.session.add(post)
    db.session.commit()

    if es.ping():
        body = {
            'id': post.id,
            'public_id': post.public_id,
            'title': post.title,
            'description': post.description,
            'city_address': post.city_address,
            'district_address': post.district_address,
            'detailed_address': post.detailed_address,
            'latitude': post.latitude,
            'longitude': post.longitude,
            'subject': post.subject,
            'class_type': post.class_type,
            'fee': post.fee,
            'number_of_sessions': post.number_of_sessions,
            'require': post.require,
            'contact': post.contact,
            'form_of_teaching': post.form_of_teaching,
            'schedules': Schedule.to_json_list(post.schedules)
        }
        es.index(index=elasticsearch_index.LOOKING_FOR_STUDENT_POST, id=body['id'], body=body)

    return response_object(data={'post_id': post.id}), 201


def create_search_post(args, user_id):
    user = User.query.get(user_id)

    if not user:
        return response_object(status=False, message=response_message.UNAUTHORIZED_401), 401

    post = Post(
        is_tutor=False,
        public_id='BD' + str(uuid.uuid4())[:6].upper(),
        title=args['title'],
        description=args['description'],
        city_address=args['city_address'],
        district_address=args['district_address'],
        detailed_address=args['detailed_address'],
        latitude=args['latitude'],
        longitude=args['longitude'],
        subject=args['subject'],
        class_type=args['class_type'],
        other_information=args['other_information'],
        fee=args['fee'],
        # schedule=args['schedule'],
        number_of_sessions=args['number_of_sessions'],
        require=args['require'],
        contact=args['contact'],
        form_of_teaching=args['form_of_teaching'],
        user_id=user.id
    )

    db.session.add(post)

    db.session.commit()

    if es.ping():
        body = {
            'id': post.id,
            'public_id': post.public_id,
            'title': post.title,
            'description': post.description,
            'city_address': post.city_address,
            'district_address': post.district_address,
            'detailed_address': post.detailed_address,
            'latitude': post.latitude,
            'longitude': post.longitude,
            'subject': post.subject,
            'class_type': post.class_type,
            'fee': post.fee,
            'number_of_sessions': post.number_of_sessions,
            'require': post.require,
            'contact': post.contact,
            'form_of_teaching': post.form_of_teaching,
            'schedules': Schedule.to_json_list(post.schedules)
        }
        es.index(index=elasticsearch_index.LOOKING_FOR_TUTOR_POST, id=body['id'], body=body)

    return response_object(data={'post_id': post.id}), 201


def get_own_posts(args, user_id):
    user = User.query.get(user_id)
    if not user:
        return response_object(status=False, message=response_message.POST_NOT_FOUND), 404
    page = args['page']
    page_size = args['page_size']
    posts = Post.query.filter(
        or_(
            or_(Post.public_id.like("%{}%".format(args['public_id'])), args['public_id'] is None),
            Post.public_id.like("%{}%".format(args['keyword']))),
        or_(Post.is_tutor == args['is_tutor'], args['is_tutor'] is None),
        or_(
            or_(Post.title.like("%{}%".format(args['title'])), args['title'] is None),
            Post.title.like("%{}%".format(args['keyword']))),
        or_(
            or_(Post.description.like("%{}%".format(args['description'])), args['description'] is None),
            Post.description.like("%{}%".format(args['keyword']))),
        or_(
            or_(Post.city_address.like("%{}%".format(args['city_address'])), args['city_address'] is None),
            Post.city_address.like("%{}%".format(args['keyword']))),
        or_(
            or_(Post.district_address.like("%{}%".format(args['district_address'])),
                args['district_address'] is None), Post.district_address.like("%{}%".format(args['keyword']))),
        or_(
            or_(Post.detailed_address.like("%{}%".format(args['detailed_address'])),
                args['detailed_address'] is None), Post.detailed_address.like("%{}%".format(args['keyword']))),
        or_(
            or_(Post.subject.like("%{}%".format(args['subject'])), args['subject'] is None),
            Post.subject.like("%{}%".format(args['keyword']))),
        or_(
            or_(Post.other_information.like("%{}%".format(args['other_information'])),
                args['other_information'] is None), Post.other_information.like("%{}%".format(args['keyword']))),
        or_(Post.fee.like("%{}%".format(args['fee'])), args['fee'] is None),
        # or_(Post.schedule.like("%{}%".format(args['schedule'])), args['schedule'] is None),
        or_(Post.number_of_sessions.like("%{}%".format(args['number_of_sessions'])),
            args['number_of_sessions'] is None),
        or_(
            or_(Post.require.like("%{}%".format(args['require'])), args['require'] is None),
            Post.require.like("%{}%".format(args['keyword']))),
        or_(
            or_(Post.contact.like("%{}%".format(args['contact'])), args['contact'] is None),
            Post.contact.like("%{}%".format(args['keyword']))),
        or_(Post.form_of_teaching.like("%{}%".format(args['form_of_teaching'])), args['form_of_teaching'] is None),

        or_(
            or_(
                or_(Post.user.has(User.first_name.like("%{}%".format(args['user_name']))),
                    args['user_name'] is None),
                Post.user.has(User.first_name.like("%{}%".format(args['keyword']))), ),
            or_(
                or_(Post.user.has(User.last_name.like("%{}%".format(args['user_name']))),
                    args['user_name'] is None),
                Post.user.has(User.first_name.like("%{}%".format(args['keyword']))), )
        ),
        Post.user_id == user.id,
        Post.is_active
    ).order_by(Post.created_date if args['sort'] == 'oldest' else desc(Post.created_date)).paginate(page, page_size,
                                                                                                    error_out=False)
    # print(len(posts.items))
    followed_posts = Post.query.filter(Post.followed_users.any(User.id == user_id)).all()

    data = add_follow(posts.items, followed_posts)
    return response_object(data=data, pagination={'total': posts.total, 'page': posts.page}), 200


def filter_posts(args, user_id):
    page = args['page']
    page_size = args['page_size']
    keyword = args['keyword']
    id_list = []
    print('1111111111111111111111111111111')
    if keyword and keyword != '' and es.ping():
        print('222222222222')
        body = {
            "size": 1000,
            "query": {
                "multi_match": {
                    "query": keyword,
                    "fields": ["public_id", "title", "fee", "require", "form_of_teaching",
                               "degree", "school", "city_address", "district_address", "detailed_address"
                        , "subject", "class_type"]
                },
            },
        }
        if args['is_tutor']:
            res = es.search(index=elasticsearch_index.LOOKING_FOR_STUDENT_POST, body=body)
        else:
            res = es.search(index=elasticsearch_index.LOOKING_FOR_TUTOR_POST, body=body)
        res_list = res['hits']['hits']

        id_list = [re['_id'] for re in res_list]
    print(id_list)
    posts = Post.query.filter(
        Post.id.in_(id_list) if len(id_list) > 0 else True,
        or_(Post.is_tutor == args['is_tutor'], args['is_tutor'] is None),

        or_(Post.city_address.like("%{}%".format(args['city_address'])), args['city_address'] is None),

        or_(Post.district_address.like("%{}%".format(args['district_address'])),
            args['district_address'] is None),

        or_(Post.detailed_address.like("%{}%".format(args['detailed_address'])), args['detailed_address'] is None),

        or_(Post.subject.like("%{}%".format(args['subject'])), args['subject'] is None),

        or_(Post.other_information.like("%{}%".format(args['other_information'])), args['other_information'] is None),
        or_(Post.fee.like("%{}%".format(args['fee'])), args['fee'] is None),

        or_(Post.number_of_sessions.like("%{}%".format(args['number_of_sessions'])),
            args['number_of_sessions'] is None),

        or_(Post.require.like("%{}%".format(args['require'])), args['require'] is None),

        or_(Post.contact.like("%{}%".format(args['contact'])), args['contact'] is None),
        or_(Post.form_of_teaching.like("%{}%".format(args['form_of_teaching'])), args['form_of_teaching'] is None),
        or_(Post.user_id == args['user_id'], args['user_id'] is None),
        Post.status == PostStatus.OPENING,
        Post.is_active
    ).order_by(desc(Post.created_date)).paginate(page, page_size, error_out=False)

    # posts = Post.query.filter(Post.follow_users.any(Follow.user_id == user_id)).paginate(page, page_size,
    #                                                                                      error_out=False)

    followed_post = []
    try:
        user = User.query.get(user_id)
        followed_post = user.followed_posts
        data = add_follow_status(posts.items, followed_post, user.posts)
    except:
        data = add_follow_status(posts.items, followed_post)
    # data = add_follow_status(posts.items, followed_post,user.posts)

    return response_object(data=data,
                           pagination={'total': posts.total, 'page': posts.page}), 200


def add_follow(posts, followed_post):
    data_list = []
    if len(followed_post) > 0:
        for post in posts:
            data = post.to_json()

            if any(f.id == post.id for f in followed_post):
                data['followed'] = True
            else:
                data['followed'] = False

            data['by_user'] = True

            data_list.append(data)
    else:
        for post in posts:
            data = post.to_json()
            data['followed'] = False
            data['by_user'] = True
            data_list.append(data)

    return data_list


def add_follow_status(posts, followed_post, created_post=[]):
    data_list = []
    if len(followed_post) > 0:
        for post in posts:
            data = post.to_json()

            if any(f.id == post.id for f in followed_post):
                data['followed'] = True
            else:
                data['followed'] = False
            if any(p.id == post.id for p in created_post):
                data['by_user'] = True
            else:
                data['by_user'] = False
            data_list.append(data)
    else:
        for post in posts:
            data = post.to_json()
            data['followed'] = False
            if any(p.id == post.id for p in created_post):
                data['by_user'] = True
            else:
                data['by_user'] = False
            data_list.append(data)

    return data_list


def related_post(post_id):
    post = Post.query.get(post_id)

    posts = Post.query.filter(Post.subject.like("%{}%".format(post.subject))).limit(5).all()

    return response_object(data=[post.to_json for post in posts]), 200


def get_by_id(post_id, user_id):
    post = Post.query.filter(Post.id == post_id, Post.is_active).first()
    if not post:
        return response_object(status=False, message=response_message.POST_NOT_FOUND), 404
    post.number_of_viewer = (post.number_of_viewer + 1)
    db.session.commit()
    data = post.to_json()

    try:
        user = User.query.get(user_id)
        followed_posts = Post.query.filter(Post.followed_users.any(User.id == user_id)).all()
        registration = Registration.query.filter(Registration.post.has(Post.id == post_id),
                                                 Registration.author_id == user_id,
                                                 Registration.status != RegistrationStatus.CANCEL).first()
        if not registration:
            data['registered'] = False
            data['status_register'] = None
        else:
            data['registered'] = True
            data['status_register'] = registration.get_status()

        if any(f.id == post.id for f in followed_posts):
            data['followed'] = True
        else:
            data['followed'] = False
        if any(p.id == post.id for p in user.posts):
            data['by_user'] = True
        else:
            data['by_user'] = False
    except:
        data['followed'] = False
        data['by_user'] = False

    classes = Class.query.filter(
        or_(
            and_(Class.student_id == post.user_id, Class.teacher_id == user_id),
            and_(Class.teacher_id == post.user_id, Class.student_id == user_id)
        )).all()
    rate = Rate.query.filter(Rate.user_id == post.user_id, Rate.author_id == user_id).all()

    if len(classes) == 0:
        can_rate = False

    if len(classes) > len(rate):
        can_rate = True
    else:
        can_rate = False

    data['user']['can_rate'] = can_rate

    return response_object(data=data), 200


def update(args, post_id, user_id):
    user = User.query.get(user_id)
    if not user:
        return response_object(status=False, message=response_message.USER_NOT_FOUND), 404
    post = Post.query.get(post_id)
    if not post:
        return response_object(status=False, message=response_message.POST_NOT_FOUND), 404
    if post.user_id != user.id:
        return response_object(status=False, message=response_message.FORBIDDEN_403), 403
    post.title = args['title'] if args['title'] else post.title
    post.description = args['description'] if args['description'] else post.description
    post.city_address = args['city_address'] if args['city_address'] else post.city_address
    post.district_address = args['district_address'] if args['district_address'] else post.district_address
    post.detailed_address = args['detailed_address'] if args['detailed_address'] else post.detailed_address
    post.subject = args['subject'] if args['subject'] else post.subject
    post.class_type = args['class_type'] if args['class_type'] else post.class_type
    post.other_information = args['other_information'] if args['other_information'] else post.other_information
    post.fee = args['fee'] if args['fee'] else post.fee
    post.number_of_sessions = args['number_of_sessions'] if args['number_of_sessions'] else post.number_of_sessions
    post.require = args['require'] if args['require'] else post.require
    post.contact = args['contact'] if args['contact'] else post.contact
    post.form_of_teaching = args['form_of_teaching'] if args['form_of_teaching'] else post.form_of_teaching
    post.latitude = args['latitude'] if args['latitude'] else post.latitude
    post.longitude = args['longitude'] if args['longitude'] else post.longitude
    post.updated_date = datetime.now()

    for s in post.schedules:
        Schedule.query.filter(Schedule.id == s.id).delete()

    db.session.commit()
    if es.ping():
        body = {
            'id': post.id,
            'public_id': post.public_id,
            'title': post.title,
            'description': post.description,
            'city_address': post.city_address,
            'district_address': post.district_address,
            'detailed_address': post.detailed_address,
            'latitude': post.latitude,
            'longitude': post.longitude,
            'subject': post.subject,
            'class_type': post.class_type,
            'fee': post.fee,
            'number_of_sessions': post.number_of_sessions,
            'require': post.require,
            'contact': post.contact,
            'form_of_teaching': post.form_of_teaching,
            'schedules': Schedule.to_json_list(post.schedules)
        }
        es.index(
            index=elasticsearch_index.LOOKING_FOR_TUTOR_POST if not post.is_tutor else elasticsearch_index.LOOKING_FOR_STUDENT_POST,
            id=body['id'], body=body)

    return response_object(), 200


def delete(user_id, post_id):
    user = User.query.get(user_id)
    print(user)

    if not user:
        return response_object(status=False, message=response_message.USER_NOT_FOUND), 404
    post = Post.query.get(post_id)
    if not post:
        return response_object(status=False, message=response_message.POST_NOT_FOUND), 404
    if post.user_id != user.id:
        return response_object(status=False, message=response_message.FORBIDDEN_403), 403
    if not post.is_active:
        return response_object(status=False, message=response_message.POST_NOT_FOUND), 404

    # Post.query.filter(Post.id == post_id).delete()
    post.is_active = False

    db.session.commit()
    return response_object(), 200
