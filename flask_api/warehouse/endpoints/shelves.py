from typing import List, Tuple

from flask import request
from flask_restplus import Resource

from flask_api.api import api
from flask_api.app import auth

from .. import models, serializers

ns = api.namespace("shelves")


@ns.route("/")
class ShelfCollection(Resource):
    @auth.login_required
    @api.marshal_list_with(serializers.shelf)
    def get(self) -> List[models.Shelf]:
        shelves = models.Shelf.query.all()
        return shelves

    @auth.login_required
    @api.expect(serializers.shelf)
    @api.marshal_with(serializers.shelf)
    def post(self) -> Tuple[models.Shelf, int]:
        data = request.json
        shelf = models.Shelf.create(data)
        return shelf, 201


@ns.route("/<int:pk>/")
@api.response(404, "Shelf not found.")
class ShelfItem(Resource):
    @auth.login_required
    @api.marshal_with(serializers.shelf)
    def get(self, pk: int) -> models.Organization:
        return models.Shelf.query.filter(models.Shelf.id == pk).one()

    @auth.login_required
    @api.expect(serializers.shelf)
    @api.marshal_with(serializers.shelf)
    def put(self, pk: int) -> Tuple[models.Shelf, int]:
        data = request.json
        shelf = models.Shelf.update(pk, data)
        return shelf, 204

    @auth.login_required
    @api.response(204, "Successfully deleted.")
    def delete(self, pk: int) -> Tuple[None, int]:
        models.Shelf.delete(pk)
        return None, 204
