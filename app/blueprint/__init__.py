import werkzeug
from flask import Blueprint
from flask_restx import Api

from app.controller.demo_controller import api as demo_api
from app.controller.user_controller import api as user_api
from app.util.api_response import response_object

blueprint = Blueprint('api', __name__, url_prefix="/api", template_folder='templates')
api = Api(blueprint,
          title='API DOCUMENT FOR TUTOR SEARCH SYSTEM',
          version='1.0'
          )

api.add_namespace(demo_api, path='/demo')
api.add_namespace(user_api, path='/user')


@api.errorhandler(werkzeug.exceptions.BadRequest)
def bad_request(error):
    return response_object(code=403, status=False, message='Bad Request'), 403


@api.errorhandler(werkzeug.exceptions.Forbidden)
def forbidden(error):
    return response_object(code=403, status=False, message='Forbidden'), 403


@api.errorhandler(werkzeug.exceptions.NotFound)
def page_not_found(error):
    return response_object(code=404, status=False, message='Page Not Found'), 404


@api.errorhandler(werkzeug.exceptions.InternalServerError)
def internal_server_error(error):
    return response_object(code=500, status=False, message='Server Error'), 500
