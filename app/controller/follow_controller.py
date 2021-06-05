from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restx import Resource

from app import db
from app.dto.follow_dto import FollowDto
from app.dto.post_dto import PostDto
# from app.model.follow import follow_table
from app.model.follow import Follow
from app.model.post_model import Post
from app.model.user_model import User
from app.util import response_message
from app.util.api_response import response_object
from app.util.auth_parser_util import get_auth_required_parser

api = FollowDto.api


@api.route('/<int:post_id>')
class FollowController(Resource):
    @api.doc('follow post')
    @api.response(200, 'OK')
    @api.response(401, 'Unauthorized')
    @api.response(403, 'Forbidden')
    @api.response(404, 'Not found')
    @api.response(500, 'Internal server error')
    @api.expect(get_auth_required_parser(api), validate=True)
    @jwt_required()
    def post(self, post_id):
        """follow và unfollow bài post"""
        user_id = get_jwt_identity()['user_id']
        user = User.query.get(user_id)
        if not user:
            return response_object(status=False, message=response_message.USER_NOT_FOUND), 404
        post = Post.query.get(post_id)
        if not post:
            return response_object(status=False, message=response_message.POST_NOT_FOUND), 404
        if post in user.follow_posts:
            user.follow_posts.remove(post)
        else:
            user.follow_posts.append(post)
        db.session.commit()
        return response_object(), 200


_filter_response = PostDto.post_list_response


@api.route('')
class FollowListController(Resource):

    @api.doc('get list followed post')
    @api.response(200, 'OK')
    @api.response(401, 'Unauthorized')
    @api.response(403, 'Forbidden')
    @api.response(404, 'Not found')
    @api.response(500, 'Internal server error')
    @api.expect(get_auth_required_parser(api), validate=True)
    @api.marshal_with(_filter_response, 200)
    @jwt_required()
    def get(self):
        """filter các bài post đã follow"""
        user_id = get_jwt_identity()['user_id']
        user = User.query.get(user_id)
        page = 0
        page_size = 15
        if not user:
            return response_object(status=False, message=response_message.USER_NOT_FOUND), 404

        posts = Post.query.filter(Post.follow_users.any(Follow.user_id == user_id)).paginate(page, page_size,
                                                                                             error_out=False)

        return response_object(data=[post.to_json() for post in posts.items],
                               pagination={'total': posts.total, 'page': posts.page}), 200
