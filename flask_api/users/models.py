from typing import Optional

from flask import current_app as app
from itsdangerous import BadSignature, JSONWebSignatureSerializer as Serializer

from flask_api.database import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True)

    @property
    def auth_token(self) -> str:
        s = Serializer(app.config["SECRET_KEY"])
        return s.dumps({"id": self.id})

    @staticmethod
    def verify_auth_token(token: str) -> Optional["User"]:
        s = Serializer(app.config["SECRET_KEY"])
        try:
            data = s.loads(token)
        except BadSignature:
            return None  # invalid token
        user = User.query.get(data["id"])
        return user

    @classmethod
    def create(cls, data: dict) -> "User":
        username = data.get("username")
        user = cls(username=username)
        db.session.add(user)
        db.session.commit()
        return user
