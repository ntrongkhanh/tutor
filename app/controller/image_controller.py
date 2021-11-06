from flask_jwt_extended import get_jwt_identity, jwt_required, verify_jwt_in_request
from flask_restx import Resource

from app.dto.image_dto import ImageDto
from app.service import image_service
from app.util.auth_parser_util import get_auth_not_required_parser, get_auth_required_parser

api = ImageDto.api
_message_response = ImageDto.message_response

_create_request = ImageDto.create_parser
_create_response = ImageDto.image_response

_upload_request = ImageDto.upload_parser
_upload_response = ImageDto.image_response

_delete_request = get_auth_required_parser(api)

_filter_request = ImageDto.filter_parser
_filter_response = ImageDto.image_list_response


@api.route('')
class ImageListController(Resource):
    @api.doc('filter')
    @api.expect(_filter_request, validate=True)
    # @api.marshal_with(_filter_response, 200)
    def get(self):
        """Filter images (Lọc hình ảnh)"""
        args = _filter_request.parse_args()

        try:
            verify_jwt_in_request()
            user_id = get_jwt_identity()['user_id']
        except:
            user_id = None
        return image_service.filter_image(args, user_id)

    @api.doc('create image')
    @api.expect(_create_request, validate=True)
    # @api.marshal_with(_create_response, 201)
    def post(self):
        """Create new image (Upload hình ảnh)"""
        args = _create_request.parse_args()
        return image_service.create(args)


@api.route('/<int:image_id>')
class ImageController(Resource):
    @api.doc('get image')
    @api.response(200, 'OK')
    @api.response(404, 'Not found')
    @api.response(500, 'Internal server error')
    @api.expect(get_auth_not_required_parser(api))
    def get(self, image_id):
        """Get image by id  (Get hình ảnh by id)"""
        try:
            verify_jwt_in_request()
            user_id = get_jwt_identity()['user_id']
        except:
            user_id = None

        return image_service.get_by_id(image_id, user_id)

    @api.doc('update image')
    @api.expect(_upload_request, validate=True)
    @api.response(401, 'Unauthorized')
    @api.response(403, 'Forbidden')
    @api.response(404, 'Not found')
    @api.response(500, 'Internal server error')
    # @api.marshal_with(_create_response, 200)
    @jwt_required()
    def put(self):
        """Update an image (Cập nhật hình ảnh)"""
        user_id = get_jwt_identity()['user_id']
        args = _upload_request.parse_args()
        return image_service.update(args, user_id)
