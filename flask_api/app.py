from flask import Blueprint, Flask

from flask_api import database, settings
from flask_api.api import api

from .users.auth import auth  # NOQA

app = Flask(__name__)


def configure_app(flask_app: Flask) -> None:
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = settings.SQLALCHEMY_DATABASE_URI
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = settings.SQLALCHEMY_TRACK_MODIFICATIONS
    flask_app.config["RESTPLUS_VALIDATE"] = settings.RESTPLUS_VALIDATE
    flask_app.config["SECRET_KEY"] = settings.SECRET_KEY


def initialize_app(flask_app: Flask) -> None:
    from flask_api.warehouse.endpoints.boxes import ns as boxes_ns
    from flask_api.warehouse.endpoints.organizations import ns as organizations_ns
    from flask_api.warehouse.endpoints.shelves import ns as shelves_ns
    from flask_api.users.endpoints.users import ns as users_ns

    configure_app(flask_app)

    blueprint = Blueprint("api", __name__, url_prefix="")
    api.init_app(blueprint)
    api.add_namespace(users_ns)
    api.add_namespace(boxes_ns)
    api.add_namespace(organizations_ns)
    api.add_namespace(shelves_ns)
    flask_app.register_blueprint(blueprint)

    database.db.init_app(flask_app)


def main() -> None:
    initialize_app(app)
    app.run(debug=settings.FLASK_DEBUG)


if __name__ in ["__main__", "flask_api.app"]:
    main()
