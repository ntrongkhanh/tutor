from flask import Blueprint
from flask_restx import Api

from app.controller.demo_controller import api as demo_api
from app.controller.user_controller import api as user_api

blueprint = Blueprint('api', __name__, url_prefix="/api", template_folder='templates')
api = Api(blueprint,
          title='API DOCUMENT FOR TUTOR SEARCH SYSTEM',
          version='1.0'
          )

api.add_namespace(demo_api, path='/demo')
api.add_namespace(user_api, path='/user')
