from src.external_interfaces.flask_server.settings import DevConfig

from flask_openapi3 import OpenAPI, Info
from flask_cors import CORS
from .register_route import register_route


def create_app(config_object=DevConfig):
    """Creates the server

    Args:
        config_object (object, optional): Defaults to DevConfig.
            Adds a config when creating the app server

    Returns:
        class 'flask.app.Flask': A Flask app
    """

    info = Info(title="Minha API", version="1.0.0")
    app = OpenAPI(
        __name__,
        info=info,
    )
    CORS(app)
    return app
