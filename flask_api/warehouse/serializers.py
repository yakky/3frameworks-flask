from flask_restplus import fields

from flask_api.api import api

organization = api.model("Organization", {"id": fields.Integer(readOnly=True), "name": fields.String(required=True)})

shelf = api.model(
    "Shelf",
    {
        "id": fields.Integer(readOnly=True),
        "size": fields.Integer(),
        "available_size": fields.Integer(readOnly=True),
        "organization_id": fields.Integer(attribute="organization.id"),
    },
)

box = api.model("Box", {"id": fields.Integer(readOnly=True), "shelf_id": fields.Integer(attribute="shelf.id")})
