import flask

import app.util.response_message as message
from app.model.image_model import Image
from app.util.api_response import response_object


def get_post_by_id(image_id):
    image = Image.query.get(image_id)
    if not image:
        return response_object(status=False, message=message.NOT_FOUND_404), 404
    image_binary = image.data
    response = flask.make_response(image_binary)
    response.headers.set('Content-Type', 'image/jpeg')
    response.headers.set('Content-Disposition', 'inline')  # inline attachment
    return response
