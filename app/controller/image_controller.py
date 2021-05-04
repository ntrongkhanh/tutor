import flask
from flask_restx import Resource

from app.dto.image_dto import ImageDto
from app.model.image_model import Image
from app.service import image_service as service

api = ImageDto.api

get_by_id = api.parser()
get_by_id.add_argument('id', type=int, location='args', required=True)


@api.route("/get/")
class get(Resource):
    @api.doc('get user')
    @api.expect(get_by_id, validate=True)
    @api.marshal_with(ImageDto.image_response, 200)
    def get(self):
        args = get_by_id.parse_args()

        return service.get_post_by_id(args['id'])

