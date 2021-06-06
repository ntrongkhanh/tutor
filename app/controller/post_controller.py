import uuid
from datetime import datetime
from operator import or_

from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request
from flask_restx import Resource
from sqlalchemy import desc

import app.util.response_message as response_message
from app import db
from app.dto.post_dto import PostDto
from app.model.post_model import Post
from app.model.user_model import User
from app.util.api_response import response_object
from app.util.auth_parser_util import get_auth_required_parser, get_auth_not_required_parser
from app.util.jwt_util import tutor_required

api = PostDto.api

_create_request = PostDto.create_parser

_update_request = PostDto.update_parser

_filter_request = PostDto.filter_parser

_filter_response = PostDto.post_list_response

_post_response = PostDto.post_response

_post_request = get_auth_not_required_parser(api)


# ok
# chưa jwt , truyền user vào
@api.route('/create-tutor-post')
class CreateTutorPost(Resource):
    @api.doc('create tutor post')
    @api.expect(_create_request, validate=True)
    @api.response(201, 'Created')
    @api.response(401, 'Unauthorized')
    @api.response(403, 'Forbidden')
    @api.response(404, 'Not found')
    @api.response(500, 'Internal server error')
    @jwt_required()
    @tutor_required()
    def post(self):
        """Create tutor post (Gia sư tạo bài đăng)"""

        args = _create_request.parse_args()
        user = User.query.get(get_jwt_identity()['user_id'])
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
            subject=args['subject'],
            class_type=args['class_type'],
            other_information=args['other_information'],
            fee=args['fee'],
            schedule=args['schedule'],
            number_of_sessions=args['number_of_sessions'],
            require=args['require'],
            contact=args['contact'],
            form_of_teaching=args['form_of_teaching'],
            user_id=user.id
        )
        db.session.add(post)
        db.session.commit()

        return response_object(), 201


# ok
# chưa jwt , truyền user vào
@api.route('/create-search-post')
class CreateSearchPost(Resource):
    @api.doc('create search post')
    @api.expect(_create_request, validate=True)
    @api.response(201, 'Created')
    @api.response(401, 'Unauthorized')
    @api.response(403, 'Forbidden')
    @api.response(404, 'Not found')
    @api.response(500, 'Internal server error')
    @jwt_required()
    def post(self):
        """Create search post (Đăng bài tìm kiếm gia sư)"""

        args = _create_request.parse_args()
        user = User.query.get(get_jwt_identity()['user_id'])

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
            subject=args['subject'],
            class_type=args['class_type'],
            other_information=args['other_information'],
            fee=args['fee'],
            schedule=args['schedule'],
            number_of_sessions=args['number_of_sessions'],
            require=args['require'],
            contact=args['contact'],
            form_of_teaching=args['form_of_teaching'],
            user_id=user.id
        )

        db.session.add(post)

        db.session.commit()

        return response_object(), 201


@api.route('')
class PostListController(Resource):
    # ok
    @api.doc('filter post')
    @api.expect(_filter_request, validate=True)
    @api.response(401, 'Unauthorized')
    @api.response(403, 'Forbidden')
    @api.response(404, 'Not found')
    @api.response(500, 'Internal server error')
    @api.marshal_with(_filter_response, 200)
    def get(self):
        """Filter posts (lọc các bài post)"""
        args = _filter_request.parse_args()
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
            or_(Post.schedule.like("%{}%".format(args['schedule'])), args['schedule'] is None),
            or_(Post.number_of_sessions.like("%{}%".format(args['number_of_sessions'])),
                args['number_of_sessions'] is None),
            or_(
                or_(Post.require.like("%{}%".format(args['require'])), args['require'] is None),
                Post.require.like("%{}%".format(args['keyword']))),
            or_(
                or_(Post.contact.like("%{}%".format(args['contact'])), args['contact'] is None),
                Post.contact.like("%{}%".format(args['keyword']))),
            or_(Post.form_of_teaching.like("%{}%".format(args['form_of_teaching'])), args['form_of_teaching'] is None),
            or_(Post.user_id == args['user_id'], args['user_id'] is None),
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
            Post.is_active
        ).order_by(desc(Post.created_date)).paginate(page, page_size, error_out=False)

        # posts = Post.query.filter(Post.follow_users.any(Follow.user_id == user_id)).paginate(page, page_size,
        #                                                                                      error_out=False)
        followed_post = []
        try:
            verify_jwt_in_request()
            user = User.query.get(get_jwt_identity()['user_id'])
            followed_post = user.follow_posts
            data = add_follow_status(posts.items, followed_post, user.posts)
        except:
            data = add_follow_status(posts.items, followed_post)
        # data = add_follow_status(posts.items, followed_post,user.posts)
        return response_object(data=data,
                               pagination={'total': posts.total, 'page': posts.page}), 200

        # return response_object(data=[post.to_json() for post in posts.items],
        #                        pagination={'total': posts.total, 'page': posts.page}), 200


def add_follow_status(posts, followed_post,created_post=[]):
    data_list = []
    if len(followed_post) > 0:
        for post in posts:
            data = post.to_json()

            if any(f.id == post.id for f in followed_post):
                data['followed'] = True
            else:
                data['followed'] = False
            if any(p.id==post.id for p in created_post):
                data['by_user'] = True
            else:
                data['by_user'] = False
            data_list.append(data)
    else:
        for post in posts:
            data = post.to_json()
            data['followed'] = False
            if any(p.id==post.id for p in created_post):
                data['by_user'] = True
            else:
                data['by_user'] = False
            data_list.append(data)

    return data_list


@api.route('/<int:post_id>')
class PostController(Resource):

    # chưa load user lên
    @api.doc('get post by id')
    @api.response(401, 'Unauthorized')
    @api.response(403, 'Forbidden')
    @api.response(404, 'Not found')
    @api.response(500, 'Internal server error')
    @api.expect(get_auth_required_parser(api),validate=True)
    @api.marshal_with(_post_response, 200)
    def get(self, post_id):
        """Get a post by id (Get bài post)"""
        post = Post.query.filter(Post.id == post_id, Post.is_active).first()
        if not post:
            return response_object(status=False, message=response_message.POST_NOT_FOUND), 404

        data = post.to_json()


        try:
            verify_jwt_in_request()
            user = User.query.get(get_jwt_identity()['user_id'])
            followed_post = user.follow_posts
            if any(f.id == post.id for f in followed_post):
                print(followed_post)
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

        return response_object(data=data), 200

    # chưa test
    @api.doc('update post')
    @api.expect(_update_request, validate=True)
    @api.response(200, 'OK')
    @api.response(401, 'Unauthorized')
    @api.response(403, 'Forbidden')
    @api.response(404, 'Not found')
    @api.response(500, 'Internal server error')
    @jwt_required()
    @tutor_required()
    def put(self, post_id):
        """Update post (Cập nhật bài post)"""
        args = _update_request.parse_args()

        user = User.query.get(get_jwt_identity()['user_id'])
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
        post.schedule = args['schedule'] if args['schedule'] else post.schedule
        post.number_of_sessions = args['number_of_sessions'] if args['number_of_sessions'] else post.number_of_sessions
        post.require = args['require'] if args['require'] else post.require
        post.contact = args['contact'] if args['contact'] else post.contact
        post.form_of_teaching = args['form_of_teaching'] if args['form_of_teaching'] else post.form_of_teaching
        post.updated_date = datetime.now()
        db.session.commit()

        return response_object(), 200

    # ok
    # chưa jwt
    @api.doc('delete post')
    @api.response(200, 'OK')
    @api.response(401, 'Unauthorized')
    @api.response(403, 'Forbidden')
    @api.response(404, 'Not found')
    @api.response(500, 'Internal server error')
    @api.expect(get_auth_required_parser(api), validate=True)
    @jwt_required()
    @tutor_required()
    def delete(self, post_id):
        """Delete post by id (Xóa bài post)"""
        user = User.query.get(get_jwt_identity()['user_id'])
        if not user:
            return response_object(status=False, message=response_message.USER_NOT_FOUND), 404
        post = Post.query.get(post_id)
        if not post:
            return response_object(status=False, message=response_message.POST_NOT_FOUND), 404
        if post.user_id != user.id:
            return response_object(status=False, message=response_message.FORBIDDEN_403), 403
        # Post.query.filter(Post.id == post_id).delete()
        post.is_active = False

        db.session.commit()
        return response_object(), 200
