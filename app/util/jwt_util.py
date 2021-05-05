# imports for PyJWT authentication
from functools import wraps

from flask import request, jsonify

from app.model.user_model import User
from app.util.api_response import response_object
from app.util.response_message import UNAUTHORIZED


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
