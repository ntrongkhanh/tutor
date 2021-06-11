from datetime import datetime
from operator import or_

import flask
from flask_jwt_extended import get_jwt_identity, jwt_required, verify_jwt_in_request
from flask_restx import Resource
from werkzeug.utils import redirect

from app import db
from app.dto.image_dto import ImageDto
from app.model.image_model import Image
from app.model.user_model import User
from app.util import response_message
from app.util.api_response import response_object
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
        return filter_image(args, user_id)

    @api.doc('create image')
    @api.expect(_create_request, validate=True)
    # @api.marshal_with(_create_response, 201)
    def post(self):
        """Create new image (Upload hình ảnh)"""
        args = _create_request.parse_args()
        return create(args)


def create(args):
    file = args['file'].read()
    description = args['description']

    image = Image(data=file, description=description)
    db.session.add(image)
    db.session.commit()

    return response_object(data=image.to_json()), 201


def filter_image(args, user_id):
    image_id = args['id']
    description = args['description']
    search = "%{}%".format(description)
    page = args['page']
    page_size = args['page_size']
    if user_id:
        user = User.query.get(user_id)
        if user and user.is_admin:
            is_public = False
        else:
            is_public = True
    else:
        is_public = True

    images = Image.query.filter(
        or_(Image.description.like(search), description is None),
        or_(Image.id == image_id, image_id is None),
        Image.is_public if is_public else None
    ).paginate(page, page_size, error_out=False)

    # return None
    return response_object(data=[image.to_json() for image in images.items],
                           pagination={'total': images.total, 'page': images.page}), 200


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

        return get_by_id(image_id, user_id)

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
        return update(args, user_id)

    # @api.doc('delete image')
    # @api.response(401, 'Unauthorized')
    # @api.response(403, 'Forbidden')
    # @api.response(404, 'Not found')
    # @api.response(500, 'Internal server error')
    # @api.expect(_delete_request, validate=True)
    # #@api.marshal_with(_message_response, 200)
    # def delete(self, image_id):
    #     """Delete an image (Xóa hình ảnh)"""
    #     Image.query.filter(Image.id == image_id).delete()
    #     db.session.commit()
    #     return response_object(), 200


def get_by_id(image_id, user_id):
    image = Image.query.get(image_id)
    if not image:
        return response_object(status=False, message=response_message.NOT_FOUND_404), 404

    if not image.is_public:
        try:
            user = User.query.get(user_id)
            if image.tutor_id != user.tutor_id and not user.is_admin:
                return response_object(status=False, message=response_message.UNAUTHORIZED_401), 401
        except Exception as e:
            print(e)
            return response_object(status=False, message=response_message.UNAUTHORIZED_401), 401
    if image.link:
        return redirect(image.link)

    if not image.data:
        return response_object(status=False, message=response_message.NOT_FOUND_404), 404
    image_binary = image.data
    response = flask.make_response(image_binary)
    response.headers.set('Content-Type', 'image/jpeg')
    response.headers.set('Content-Disposition', 'inline')  # inline attachment
    return response


def update(args, user_id):
    user = User.query.get(user_id)
    if not user:
        return response_object(status=False, data=response_message.USER_NOT_FOUND), 404

    image_id = args['id']
    image = Image.query.get(image_id)
    if not image:
        return response_object(status=False, data=response_message.NOT_FOUND_404), 404

    if image.tutor_id != user.tutor_id:
        return response_object(status=False, data=response_message.FORBIDDEN_403), 403

    image.description = args['description'] if args['description'] else image.description
    image.data = args['file'].read()
    image.updated_date = datetime.now()
    db.session.commit()
    return response_object(data=image.to_json()), 200
