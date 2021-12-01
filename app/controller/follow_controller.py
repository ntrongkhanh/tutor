from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restx import Resource

from app.dto.follow_dto import FollowDto
from app.dto.post_dto import PostDto
# from app.model.follow import follow_table
from app.service import follow_service
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
        return follow_service.create(user_id, post_id)


_filter_response = PostDto.post_list_response
_filter_parser = FollowDto.filter_parser


@api.route('')
class FollowListController(Resource):
    @api.doc('get list followed post')
    @api.expect(_filter_parser, validate=True)
    # @api.marshal_with(_filter_response, 200)
    @jwt_required()
    def get(self):
        """filter các bài post đã follow"""
        user_id = get_jwt_identity()['user_id']
        args = _filter_parser.parse_args()
        return follow_service.filter_followed_post(args, user_id)


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
        return follow_service.get_followed_user_list(args, user_id)


@api.route('/followed')
class FollowedIdListController(Resource):
    @api.doc('get list id followed post')
    @api.expect(get_auth_required_parser(api), validate=True)
    @jwt_required()
    def get(self):
        """filter các bài post đã follow"""
        user_id = get_jwt_identity()['user_id']
        return follow_service.get_post_id_list(user_id)
