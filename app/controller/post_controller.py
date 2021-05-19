import uuid
from operator import or_

from flask_restx import Resource

import app.util.response_message as response_message
from app import db
from app.dto.post_dto import PostDto
from app.model.post_model import Post
from app.model.user_model import User
from app.util.api_response import response_object
from app.util.auth_parser_util import get_auth_required_parser, get_auth_not_required_parser

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
    def post(self):
        """Create tutor post (Gia sư tạo bài đăng)"""
        args = _create_request.parse_args()
        user = User.query.get(1)
        if not user.is_tutor:
            return response_object(status=False, message=response_message.FORBIDDEN), 403
        post = Post(
            public_id=str(uuid.uuid4())[:8].upper(),
            is_tutor=True,
            title=args['title'],
            description=args['description'],
            teaching_address=args['teaching_address'],
            subject=args['subject'],
            class_type=args['class_type'],
            other_information=args['other_information'],
            fee=args['fee'],
            schedule=args['schedule'],
            number_of_sessions=args['number_of_sessions'],
            require=args['require'],
            contact=args['contact'],
            form_of_teaching=args['form_of_teaching'],
            user_id=1
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
    def post(self):
        """Create search post (Đăng bài tìm kiếm gia sư)"""
        args = _create_request.parse_args()
        post = Post(
            is_tutor=False,
            public_id=str(uuid.uuid4())[:8].upper(),
            title=args['title'],
            description=args['description'],
            teaching_address=args['teaching_address'],
            subject=args['subject'],
            class_type=args['class_type'],
            other_information=args['other_information'],
            fee=args['fee'],
            schedule=args['schedule'],
            number_of_sessions=args['number_of_sessions'],
            require=args['require'],
            contact=args['contact'],
            form_of_teaching=args['form_of_teaching'],
            user_id=1
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
            or_(Post.id == args['id'], args['id'] is None),
            or_(Post.is_tutor == args['is_tutor'], args['is_tutor'] is None),
            or_(Post.title.like("%{}%".format(args['title'])), args['title'] is None),
            or_(Post.description.like("%{}%".format(args['description'])), args['description'] is None),
            or_(Post.teaching_address.like("%{}%".format(args['teaching_address'])), args['teaching_address'] is None),
            or_(Post.subject.like("%{}%".format(args['subject'])), args['subject'] is None),
            or_(Post.other_information.like("%{}%".format(args['other_information'])),
                args['other_information'] is None),
            or_(Post.fee.like("%{}%".format(args['fee'])), args['fee'] is None),
            or_(Post.schedule.like("%{}%".format(args['schedule'])), args['schedule'] is None),
            or_(Post.number_of_sessions.like("%{}%".format(args['number_of_sessions'])),
                args['number_of_sessions'] is None),
            or_(Post.require.like("%{}%".format(args['require'])), args['require'] is None),
            or_(Post.contact.like("%{}%".format(args['contact'])), args['contact'] is None),
            or_(Post.form_of_teaching.like("%{}%".format(args['form_of_teaching'])), args['form_of_teaching'] is None),
            or_(Post.user_id == args['user_id'], args['user_id'] is None),
            or_(
                or_(Post.user.has(User.first_name.like("%{}%".format(args['user_name']))), args['user_name'] is None),
                or_(Post.user.has(User.last_name.like("%{}%".format(args['user_name']))), args['user_name'] is None)
            )
        ).paginate(page, page_size, error_out=False)

        return response_object(data=[post.to_json() for post in posts.items],
                               pagination={'total': posts.total, 'page': posts.page}), 200


@api.route('/<int:post_id>')
class PostController(Resource):


    # chưa load user lên
    @api.doc('get post by id')
    @api.response(401, 'Unauthorized')
    @api.response(403, 'Forbidden')
    @api.response(404, 'Not found')
    @api.response(500, 'Internal server error')
    @api.marshal_with(_post_response, 200)
    def get(self, post_id):
        """Get a post by id (Get bài post)"""
        post = Post.query.get(post_id)

        return response_object(data=post.to_json()), 200

    # ok
    # chưa jwt, get user lên so sánh có phải là post của nó hay k
    @api.doc('update post')
    @api.expect(_update_request, validate=True)
    @api.response(200, 'OK')
    @api.response(401, 'Unauthorized')
    @api.response(403, 'Forbidden')
    @api.response(404, 'Not found')
    @api.response(500, 'Internal server error')
    def put(self):
        """Update post (Cập nhật bài post)"""
        args = _update_request.parse_args()
        post = Post.query.get(args['id'])
        if not post:
            return response_object(status=False, message=response_message.NOT_FOUND), 404

        post.title = args['title'] if args['title'] else post.title
        post.description = args['description'] if args['description'] else post.description
        post.teaching_address = args['teaching_address'] if args['teaching_address'] else post.teaching_address
        post.subject = args['subject'] if args['subject'] else post.subject
        post.class_type = args['class_type'] if args['class_type'] else post.class_type
        post.other_information = args['other_information'] if args['other_information'] else post.other_information
        post.fee = args['fee'] if args['fee'] else post.fee
        post.schedule = args['schedule'] if args['schedule'] else post.schedule
        post.number_of_sessions = args['number_of_sessions'] if args['number_of_sessions'] else post.number_of_sessions
        post.require = args['require'] if args['require'] else post.require
        post.contact = args['contact'] if args['contact'] else post.contact
        post.form_of_teaching = args['form_of_teaching'] if args['form_of_teaching'] else post.form_of_teaching

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
    def delete(self, post_id):
        """Delete post by id (Xóa bài post)"""
        Post.query.filter(Post.id == post_id).delete()
        db.session.commit()
        return response_object(), 200
