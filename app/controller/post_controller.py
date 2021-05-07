from operator import or_

from flask_restx import Resource

import app.util.response_message as response_message
from app import db
from app.dto.post_dto import PostDto
from app.model.post_model import Post
from app.model.user_model import User
from app.util.api_response import response_object

api = PostDto.api

_create_parser = api.parser()
_create_parser.add_argument("title", type=str, location="json", required=True)
_create_parser.add_argument("description", type=str, location="json", required=False)
_create_parser.add_argument("teaching_address", type=str, location="json", required=False)
_create_parser.add_argument("subject", type=str, location="json", required=True)
_create_parser.add_argument("class_type", type=str, location="json", required=False)
_create_parser.add_argument("other_information", type=str, location="json", required=False)
_create_parser.add_argument("fee", type=int, location="json", required=True)
_create_parser.add_argument("schedule", type=str, location="json", required=False)
_create_parser.add_argument("number_of_sessions", type=str, location="json", required=False)
_create_parser.add_argument("require", type=str, location="json", required=False)
_create_parser.add_argument("contact", type=str, location="json", required=False)
_create_parser.add_argument("form_of_teaching", type=str, location="json", required=False)


@api.route('/create-tutor-post')
class CreateTutorPost(Resource):
    @api.doc('create tutor post')
    @api.expect(_create_parser, validate=True)
    @api.response(201, 'Created')
    @api.response(401, 'Unauthorized')
    @api.response(403, 'Forbidden')
    @api.response(404, 'Not found')
    @api.response(500, 'Internal server error')
    def post(self):
        """Create tutor post (Gia sư tạo bài đăng)"""
        args = _create_parser.parse_args()
        post = Post(
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


@api.route('/create-search-post')
class CreateSearchPost(Resource):
    @api.doc('create search post')
    @api.expect(_create_parser, validate=True)
    @api.response(201, 'Created')
    @api.response(401, 'Unauthorized')
    @api.response(403, 'Forbidden')
    @api.response(404, 'Not found')
    @api.response(500, 'Internal server error')
    def post(self):
        """Create search post (Đăng bài tìm kiếm gia sư)"""
        args = _create_parser.parse_args()
        post = Post(
            is_tutor=False,
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


_update_parser = api.parser()
_update_parser.add_argument("id", type=int, location="json", required=True)
_update_parser.add_argument("title", type=str, location="json", required=True)
_update_parser.add_argument("description", type=str, location="json", required=False)
_update_parser.add_argument("teaching_address", type=str, location="json", required=False)
_update_parser.add_argument("subject", type=str, location="json", required=True)
_update_parser.add_argument("class_type", type=str, location="json", required=False)
_update_parser.add_argument("other_information", type=str, location="json", required=False)
_update_parser.add_argument("fee", type=int, location="json", required=True)
_update_parser.add_argument("schedule", type=str, location="json", required=False)
_update_parser.add_argument("number_of_sessions", type=str, location="json", required=False)
_update_parser.add_argument("require", type=str, location="json", required=False)
_update_parser.add_argument("contact", type=str, location="json", required=False)
_update_parser.add_argument("form_of_teaching", type=str, location="json", required=False)


@api.route('/update')
class Update(Resource):
    @api.doc('update post')
    @api.expect(_update_parser, validate=True)
    @api.response(200, 'OK')
    @api.response(401, 'Unauthorized')
    @api.response(403, 'Forbidden')
    @api.response(404, 'Not found')
    @api.response(500, 'Internal server error')
    def put(self):
        """Update post (Cập nhật bài post)"""
        args = _update_parser.parse_args()
        post = Post.query.get(args['id'])
        if not post:
            return response_object(status=False, message=response_message.NOT_FOUND), 404

        post.title = args['title']
        post.description = args['description']
        post.teaching_address = args['teaching_address']
        post.subject = args['subject']
        post.class_type = args['class_type']
        post.other_information = args['other_information']
        post.fee = args['fee']
        post.schedule = args['schedule']
        post.number_of_sessions = args['number_of_sessions']
        post.require = args['require']
        post.contact = args['contact']
        post.form_of_teaching = args['form_of_teaching']

        db.session.commit()

        return response_object(), 200


@api.route('/delete/<post_id>')
class Delete(Resource):
    @api.doc('delete post')
    @api.response(200, 'OK')
    @api.response(401, 'Unauthorized')
    @api.response(403, 'Forbidden')
    @api.response(404, 'Not found')
    @api.response(500, 'Internal server error')
    def delete(self, post_id):
        """Delete post by id (Xóa bài post)"""
        Post.query.filter(PostDto.id == post_id).delete()
        db.session.commit()
        return response_object(), 200


_filter_parser = api.parser()
_filter_parser.add_argument("id", type=int, location="args", required=False)
_filter_parser.add_argument("title", type=str, location="args", required=False)
_filter_parser.add_argument("description", type=str, location="args", required=False)
_filter_parser.add_argument("teaching_address", type=str, location="args", required=False)
_filter_parser.add_argument("subject", type=str, location="args", required=False)
_filter_parser.add_argument("class_type", type=str, location="args", required=False)
_filter_parser.add_argument("other_information", type=str, location="args", required=False)
_filter_parser.add_argument("fee", type=int, location="args", required=False)
_filter_parser.add_argument("schedule", type=str, location="args", required=False)
_filter_parser.add_argument("number_of_sessions", type=str, location="args", required=False)
_filter_parser.add_argument("require", type=str, location="args", required=False)
_filter_parser.add_argument("contact", type=str, location="args", required=False)
_filter_parser.add_argument("form_of_teaching", type=str, location="args", required=False)
_filter_parser.add_argument("user_id", type=int, location="args", required=False)
_filter_parser.add_argument("user_name", type=str, location="args", required=False)

_filter_response = PostDto.post_list_response


@api.route('/')
class Filter(Resource):
    @api.doc('filter post')
    @api.expect(_filter_parser, validate=True)
    @api.response(401, 'Unauthorized')
    @api.response(403, 'Forbidden')
    @api.response(404, 'Not found')
    @api.response(500, 'Internal server error')
    @api.marshal_with(_filter_response, 200)
    def get(self):
        """Filter posts (lọc các bài post)"""
        args = _filter_parser.parse_args()

        posts = Post.query.filter(
            or_(Post.id == args['id'], args['id'] is None),
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
        ).all()

        for i in posts:
            print(i.user.id)

        return response_object(data=[post.to_json() for post in posts]), 200


_post_response = PostDto.post_response


@api.route('/<post_id>')
class Get(Resource):
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