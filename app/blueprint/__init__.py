import werkzeug
from flask import Blueprint
from flask_restx import Api
from flask_jwt_extended.exceptions import NoAuthorizationError
from app.controller.auth_controller import api as auth_api
from app.controller.image_controller import api as image_api
from app.controller.post_controller import api as post_api
from app.controller.tutor_controller import api as tutor_api
from app.controller.user_controller import api as user_api
from app.controller.follow_controller import api as follow_api
from app.controller.rate_controller import api as rate_api
from app.controller.schedule_controller import api as schedule_api
from app.controller.registration_controller import api as registration_api
from app.controller.elasticsearch_controller import api as elasticsearch_api
from app.util.api_response import response_object

blueprint = Blueprint('api', __name__, url_prefix="/api", template_folder='templates')
api = Api(blueprint,
          title='API DOCUMENT FOR TUTOR SEARCH SYSTEM',
          version='1.0'
          )

api.add_namespace(auth_api, path='/auth')
api.add_namespace(image_api, path='/image')
api.add_namespace(user_api, path='/user')
api.add_namespace(post_api, path='/post')
api.add_namespace(tutor_api, path='/tutor')
api.add_namespace(follow_api, path='/follow')
api.add_namespace(rate_api, path='/rate')
api.add_namespace(schedule_api, path='/schedule')
api.add_namespace(registration_api, path='/registration')
api.add_namespace(elasticsearch_api, path='/elasticsearch')


@api.errorhandler(werkzeug.exceptions.BadRequest)
def bad_request(error):
    return response_object(status=False, message='Bad Request'), 400


@api.errorhandler(werkzeug.exceptions.Unauthorized)
def bad_request(error):
    return response_object(status=False, message='Unauthorized'), 401


@api.errorhandler(werkzeug.exceptions.Forbidden)
def forbidden(error):
    return response_object(status=False, message='Forbidden'), 403


@api.errorhandler(werkzeug.exceptions.NotFound)
def page_not_found(error):
    return response_object(status=False, message='Page Not Found'), 404


@api.errorhandler(werkzeug.exceptions.InternalServerError)
def internal_server_error(error):
    return response_object(status=False, message='Server Error'), 500
