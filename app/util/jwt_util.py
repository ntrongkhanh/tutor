# imports for PyJWT authentication
import json
from functools import wraps

from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.model.user_model import User
from app.util.api_response import response_object
from app.util.response_message import UNAUTHORIZED, NOT_FOUND


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
            return response_object(status=False, message=UNAUTHORIZED), 401
        # returns the current logged in users contex to the routes
        return f(*args, user, **kwargs)

    return decorated


def admin_required():
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            identity = get_jwt_identity()
            user_id = identity['user_id']
            print(user_id)
            print('11111111111111111111111111')
            try:
                user = User.query.filter(User.id == user_id).first()
                if user.is_admin:
                    return function(*args, **kwargs)
                else:
                    return response_object(status=False, message=NOT_FOUND), 404
            except:
                return response_object(status=False, message=NOT_FOUND), 404

        return wrapper
    return decorator


def tutor_required():
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            identity = get_jwt_identity()
            user_id = identity['user_id']
            print(user_id)
            try:
                user = User.query.filter(User.id == user_id).first()
                if user.is_tutor:
                    return function(*args, **kwargs)
                else:
                    return response_object(status=False, message=NOT_FOUND), 404
            except:
                return response_object(status=False, message=NOT_FOUND), 404

        return wrapper

    # print('1111111111111111111111111111111')
    return decorator


def HR_only(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        identity = get_jwt_identity()
        admin = identity['is_admin']
        id=identity['user_id']
        if admin:
            user=User.query.filter(User.id==id).first()
            return func(*args, **kwargs)
            # return user.to_payload()
        else:
            return func(*args, **kwargs)
            # return response_object(status=False, message=NOT_FOUND), 404

    return jwt_required(wrapper)