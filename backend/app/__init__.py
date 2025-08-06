import os
from flask import Flask
from flask_cors import CORS
from .routes.health import blp
from flask_smorest import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

from .models import db

def create_app():
    """Factory to create and configure Flask app with SQLAlchemy and JWT."""
    app = Flask(__name__)
    app.url_map.strict_slashes = False
    CORS(app, resources={r"/*": {"origins": "*"}})
    app.config["API_TITLE"] = "My Flask API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config['OPENAPI_URL_PREFIX'] = '/docs'
    app.config["OPENAPI_SWAGGER_UI_PATH"] = ""
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    # Environment variable driven DB connection
    # MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE
    host = os.environ.get("MYSQL_HOST")
    port = os.environ.get("MYSQL_PORT", "3306")
    user = os.environ.get("MYSQL_USER")
    password = os.environ.get("MYSQL_PASSWORD")
    dbname = os.environ.get("MYSQL_DATABASE")
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        f"mysql+pymysql://{user}:{password}@{host}:{port}/{dbname}"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET")
    # Init extensions
    db.init_app(app)
    JWTManager(app)
    api = Api(app)
    # Register Blueprints for all APIs here
    from .routes.auth import blp as auth_blp
    from .routes.profiles import blp as profiles_blp
    from .routes.connections import blp as connections_blp
    from .routes.referrals import blp as referrals_blp
    from .routes.meetings import blp as meetings_blp
    from .routes.notifications import blp as notifications_blp

    api.register_blueprint(blp)
    api.register_blueprint(auth_blp)
    api.register_blueprint(profiles_blp)
    api.register_blueprint(connections_blp)
    api.register_blueprint(referrals_blp)
    api.register_blueprint(meetings_blp)
    api.register_blueprint(notifications_blp)
    return app

# Expose `app` for `run.py` and openapi generation for backwards compatibility
app = create_app()
