from flask_restplus import fields

from flask_api.api import api

user = api.model(
    "User",
    {
        "id": fields.Integer(readOnly=True),
        "username": fields.String(required=True),
        "auth_token": fields.String(readOnly=True),
    },
)
