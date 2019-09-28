from flask import g
from flask_httpauth import HTTPTokenAuth

auth = HTTPTokenAuth(scheme="Token")


@auth.verify_token
def verify_token(username_or_token: str) -> bool:
    from . import models

    g.user = None
    user = models.User.verify_auth_token(username_or_token)
    if not user:
        return False
    g.user = user
    return True
