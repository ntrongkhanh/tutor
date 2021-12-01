from datetime import datetime
from operator import or_

import flask
from werkzeug.utils import redirect

from app import db
from app.model.image_model import Image
from app.model.user_model import User
from app.util import response_message
from app.util.api_response import response_object


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
