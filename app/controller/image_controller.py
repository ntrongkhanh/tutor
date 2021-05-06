from datetime import datetime
from operator import or_, and_

import flask
from flask_restx import Resource
from werkzeug.datastructures import FileStorage

from app import db
from app.dto.image_dto import ImageDto
from app.model.image_model import Image
from app.util import response_message
from app.util.api_response import response_object

api = ImageDto.api

# @api.route("/get/")
# class get(Resource):
#     @api.doc('get user')
#     @api.expect(get_by_id, validate=True)
#     @api.marshal_with(ImageDto.image_response, 200)
#     def get(self):
#         args = get_by_id.parse_args()
#
#         return service.get_post_by_id(args['id'])


_create_parser = api.parser()
_create_parser.add_argument("file", type=FileStorage, location="files", required=True)
_create_parser.add_argument("description", type=str, location='args', required=True)


@api.route('/create')
class create(Resource):
    @api.doc('create image')
    @api.expect(_create_parser, validate=True)
    def post(self):
        """Create new image"""
        print('create ảnh')
        args = _create_parser.parse_args()
        file = args['file'].read()
        description = args['description']

        image = Image(data=file, description=description)
        db.session.add(image)
        db.session.commit()

        return response_object(data=image.to_json()), 201


_upload_parser = api.parser()
_upload_parser.add_argument("file", type=FileStorage, location="files", required=True)
_upload_parser.add_argument("id", type=int, location='args', required=True)
_upload_parser.add_argument("description", type=str, location='args', required=True)


@api.route('/update')
class update(Resource):
    @api.doc('update image')
    @api.expect(_upload_parser, validate=True)
    def put(self):
        """Update an image"""
        print('update ảnh')
        args = _upload_parser.parse_args()
        image_id = args['id']
        image = Image.query.get(image_id)
        if not image:
            return response_object(status=False, data=response_message.NOT_FOUND), 404

        image.description = args['description']
        image.data = args['file'].read()
        image.updated_date = datetime.now()
        db.session.commit()
        return response_object(data=image.to_json()), 200


@api.route('/delete/<id>')
class delete(Resource):
    @api.doc('delete image')
    def delete(self, id):
        """Delete an image"""
        print(f'xóa ảnh id = {id}')
        Image.query.filter(Image.id == id).delete()
        db.session.commit()
        return response_object(), 200


_filter_parser = api.parser()
_filter_parser.add_argument("id", type=int, location="args", required=False)
_filter_parser.add_argument("description", type=str, location="args", required=False)


@api.route('/')
class filter(Resource):
    @api.doc('get all')
    # @api.doc(hello_world_model)
    @api.expect(_filter_parser, validate=True)
    def get(self):
        """Filter images"""
        print('filter')
        args = _filter_parser.parse_args()
        image_id = args['id']
        description = args['description']
        search = "%{}%".format(description)
        images = Image.query.filter(

                or_(Image.description.like(search), description is None),
                or_(Image.id == image_id, image_id is None)
            ).all()

        # return None
        return response_object(data=[image.to_json() for image in images]), 200


@api.route('/<id>')
class get(Resource):
    @api.doc('get image')
    def get(self, id):
        """get image by id"""
        print(id)
        image = Image.query.get(id)
        if not image:
            return response_object(status=False, message=response_message.NOT_FOUND), 404
        image_binary = image.data
        response = flask.make_response(image_binary)
        response.headers.set('Content-Type', 'image/jpeg')
        response.headers.set('Content-Disposition', 'inline')  # inline attachment
        return response
