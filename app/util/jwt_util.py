# imports for PyJWT authentication
from functools import wraps

from flask import request, jsonify

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


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        admin = False
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]
        # return 401 if token is not passed

        if not token:
            return jsonify({'message': 'Token is missing !!'}), 401
        payload = User.decode_auth_token(token)

        try:
            user = User.query.filter(User.id == payload['user_id']).first()
            if user.is_admin:
                return f(*args, user, **kwargs)
            else:
                return response_object(status=False, message=NOT_FOUND), 404
        except:
            return response_object(status=False, message=NOT_FOUND), 404
        # returns the current logged in users contex to the routes

    return decorated


def tutor_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        print('1')
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]
        # return 401 if token is not passed
        print(token)
        if not token:
            return jsonify({'message': 'Token is missing !!'}), 401
        payload = User.decode_auth_token(token)
        print(payload)
        try:
            user = User.query.filter(User.id == payload['user_id']).first()
            print(user)
            if user.is_tutor:
                return f(*args, user, **kwargs)
            else:
                return response_object(status=False, message=NOT_FOUND), 404
        except:
            return response_object(status=False, message=NOT_FOUND), 404
        # returns the current logged in users contex to the routes

    return decorated
