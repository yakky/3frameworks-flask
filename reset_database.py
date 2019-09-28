from flask_api.app import app, initialize_app
from flask_api.database import db

initialize_app(app)
with app.app_context():
    def reset_database():
        db.drop_all()
        db.create_all()
