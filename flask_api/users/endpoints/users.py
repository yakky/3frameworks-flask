from typing import List, Tuple

from flask import request
from flask_restplus import Resource

from flask_api.api import api
from flask_api.app import auth

from .. import models, serializers

ns = api.namespace("users")


@ns.route("/")
class UserCollection(Resource):
    @auth.login_required
    @api.marshal_list_with(serializers.user)
    def get(self) -> List[models.User]:
        users = models.User.query.all()
        return users

    @auth.login_required
    @api.expect(serializers.user)
    @api.marshal_with(serializers.user)
    def post(self) -> Tuple[models.User, int]:
        data = request.json
        user = models.User.create(data)
        return user, 201
