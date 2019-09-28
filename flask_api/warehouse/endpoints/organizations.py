from typing import List, Tuple

from flask import request
from flask_restplus import Resource

from flask_api.api import api
from flask_api.app import auth

from .. import models, serializers

ns = api.namespace("organizations")


@ns.route("/")
class OrganizationCollection(Resource):
    @auth.login_required
    @api.marshal_list_with(serializers.organization)
    def get(self) -> List[models.Organization]:
        organization = models.Organization.query.all()
        return organization

    @auth.login_required
    @api.expect(serializers.organization)
    @api.marshal_with(serializers.organization)
    def post(self) -> Tuple[models.Organization, int]:
        data = request.json
        organization = models.Organization.create(data)
        return organization, 201


@ns.route("/<int:pk>/")
@api.response(404, "Organization not found.")
class OrganizationItem(Resource):
    @auth.login_required
    @api.marshal_with(serializers.organization)
    def get(self, pk: int) -> models.Organization:
        return models.Organization.query.filter(models.Organization.id == pk).one()

    @auth.login_required
    @api.expect(serializers.organization)
    @api.marshal_with(serializers.organization)
    def put(self, pk: int) -> Tuple[models.Shelf, int]:
        data = request.json
        organization = models.Organization.update(pk, data)
        return organization, 204

    @auth.login_required
    @api.response(204, "Successfully deleted.")
    def delete(self, pk: int) -> Tuple[None, int]:
        models.Organization.delete(pk)
        return None, 204
