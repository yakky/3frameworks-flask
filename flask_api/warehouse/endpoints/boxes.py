from typing import List, Tuple

from flask import request
from flask_restplus import Resource

from flask_api.api import api
from flask_api.app import auth

from .. import models, serializers

ns = api.namespace("boxes")


@ns.route("/")
class BoxCollection(Resource):
    @api.marshal_list_with(serializers.box)
    def get(self) -> List[models.Box]:
        boxes = models.Box.query.all()
        return boxes

    @api.expect(serializers.box)
    @api.marshal_with(serializers.box)
    def post(self) -> Tuple[models.Box, int]:
        data = request.json
        box = models.Box.create(data)
        return box, 201


@ns.route("/<int:pk>/")
@api.response(404, "Box not found.")
class BoxItem(Resource):
    @api.marshal_with(serializers.box)
    @auth.login_required
    def get(self, pk: int) -> models.Box:
        return models.Box.query.filter(models.Box.id == pk).one()

    @api.expect(serializers.box)
    @auth.login_required
    def put(self, pk: int) -> Tuple[models.Box, int]:
        data = request.json
        box = models.Box.update(pk, data)
        return box, 204

    @api.response(204, "Successfully deleted.")
    @auth.login_required
    def delete(self, pk: int) -> Tuple[None, int]:
        models.Box.delete(pk)
        return None, 204
