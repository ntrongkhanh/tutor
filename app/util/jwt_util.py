# imports for PyJWT authentication
from functools import wraps

from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity

from app.model.model_enum import TutorStatus
from app.model.tutor_model import Tutor
from app.model.user_model import User
from app.util.api_response import response_object
from app.util.response_message import UNAUTHORIZED_401, NOT_FOUND_404


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header

        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]
        # return 401 if token is not passed

        if not token:
            return jsonify({'message': 'Token is missing !!'}), 401
        payload = User.decode_auth_token(token)

        try:
            user = User.query.filter(User.id == payload['user_id']).first()
            # decoding the payload to fetch the stored details
            # data = jwt.decode(token, app.config['SECRET_KEY'])
            # current_user = User.query \
            #     .filter_by(public_id=data['public_id']) \
            #     .first()

        except:
            return response_object(status=False, message=UNAUTHORIZED_401), 401
        # returns the current logged in users contex to the routes
        return f(*args, user, **kwargs)

    return decorated


def admin_required():
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            identity = get_jwt_identity()
            user_id = identity['user_id']

            try:
                user = User.query.filter(User.id == user_id).first()
                if user.is_admin:
                    return function(*args, **kwargs)
                else:
                    return response_object(status=False, message=NOT_FOUND_404), 404
            except:
                return response_object(status=False, message=NOT_FOUND_404), 404

        return wrapper

    return decorator


def tutor_required():
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            identity = get_jwt_identity()
            user_id = identity['user_id']

            try:
                user = User.query.get(user_id)
                if user.is_tutor:
                    tutor = Tutor.query.get(user.tutor_id)
                    if not tutor:
                        return response_object(status=False, message=UNAUTHORIZED_401), 401
                    if tutor.status == TutorStatus.APPROVED:
                        return function(*args, **kwargs)
                else:
                    return response_object(status=False, message=UNAUTHORIZED_401), 401
            except:
                return response_object(status=False, message=NOT_FOUND_404), 404

        return wrapper

    # print('1111111111111111111111111111111')
    return decorator
