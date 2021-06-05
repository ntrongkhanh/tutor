from flask_restx import Namespace

from .base_dto import base


class FollowDto:
    api = Namespace('Follow', description="Follow")
    __base = api.model("base", base)
