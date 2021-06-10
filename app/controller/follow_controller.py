from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request
from flask_restx import Resource

from app import db
from app.dto.follow_dto import FollowDto
from app.dto.post_dto import PostDto
# from app.model.follow import follow_table
from app.model.follow_model import Follow
from app.model.post_model import Post
from app.model.user_model import User
from app.util import response_message
from app.util.api_response import response_object
from app.util.auth_parser_util import get_auth_required_parser

api = FollowDto.api


@api.route('/<int:post_id>')
class FollowController(Resource):
    @api.doc('follow post')
    @api.expect(get_auth_required_parser(api), validate=True)
    @jwt_required()
    def post(self, post_id):
        """follow và unfollow bài post"""
        user_id = get_jwt_identity()['user_id']
        return create(user_id, post_id)


def create(user_id, post_id):
    user = User.query.get(user_id)
    if not user:
        return response_object(status=False, message=response_message.USER_NOT_FOUND), 404
    post = Post.query.get(post_id)
    if not post:
        return response_object(status=False, message=response_message.POST_NOT_FOUND), 404
    if post in user.followed_posts:
        user.followed_posts.remove(post)
    else:
        user.followed_posts.append(post)

    post.number_of_follower = len(post.followed_users)
    db.session.commit()
    return response_object(), 200


_filter_response = PostDto.post_list_response
_filter_parser = FollowDto.filter_parser


@api.route('')
class FollowListController(Resource):
    @api.doc('get list followed post')
    @api.expect(_filter_parser, validate=True)
    #@api.marshal_with(_filter_response, 200)
    @jwt_required()
    def get(self):
        """filter các bài post đã follow"""
        user_id = get_jwt_identity()['user_id']
        args = _filter_parser.parse_args()
        return filter_followed_post(args, user_id)


def filter_followed_post(args, user_id):
    user = User.query.get(user_id)
    page = args['page']
    page_size = args['page_size']
    if not user:
        return response_object(status=False, message=response_message.USER_NOT_FOUND), 404

    posts = Post.query.filter(Post.followed_users.any(Follow.user_id == user_id)).paginate(page, page_size,
                                                                                           error_out=False)
    followed_post = []
    try:
        verify_jwt_in_request()
        user = User.query.get(get_jwt_identity()['user_id'])
        followed_post = user.followed_posts
        data = add_follow_status(posts.items, followed_post, user.posts)
    except:
        data = add_follow_status(posts.items, followed_post)

    return response_object(data=data,
                           pagination={'total': posts.total, 'page': posts.page}), 200


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


_filter_user_parser = FollowDto.filter_user_parser


@api.route('/user')
class UserListController(Resource):
    @api.doc('get list user followed post')
    @api.expect(_filter_user_parser, validate=True)
    @jwt_required()
    def get(self):
        """filter các bài post đã follow"""
        user_id = get_jwt_identity()['user_id']
        args = _filter_user_parser.parse_args()
        return get_followed_user_list(args, user_id)


def get_followed_user_list(args, user_id):
    user = User.query.get(user_id)
    page = args['page']
    page_size = args['page_size']
    # is_tutor = True if args['tutor'] == 'true' else False

    post_id = args['post_id']
    user_list = []

    if post_id and any(post_id == p.id for p in user.posts):
        post = Post.query.get(post_id)
        user_list = post.followed_users

    total = len(user_list)
    user_list = user_list[(page - 1) * page_size:page_size + (page - 1) * page_size]

    return response_object(data=[user.to_json() for user in user_list],
                           pagination={'total': total, 'page': page}), 200


@api.route('/followed')
class FollowedIdListController(Resource):
    @api.doc('get list id followed post')
    @api.expect(get_auth_required_parser(api), validate=True)
    @jwt_required()
    def get(self):
        """filter các bài post đã follow"""
        user_id = get_jwt_identity()['user_id']
        return get_post_id_list(user_id)


def get_post_id_list(user_id):
    post_ids = get_list_followed_post(user_id)
    return response_object(data=post_ids), 200


def get_list_followed_post(user_id):
    user = User.query.get(user_id)

    if not user:
        return response_object(status=False, message=response_message.USER_NOT_FOUND), 404

    return [p.id for p in user.followed_posts]
