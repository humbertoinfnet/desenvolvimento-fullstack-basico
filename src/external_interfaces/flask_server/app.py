"""It creates the flask server with an environment and returns the server"""

from flask import Flask

from src.external_interfaces.flask_server.routers import arxiv_document
from src.external_interfaces.flask_server.routers import home
from src.external_interfaces.flask_server.settings import DevConfig

from flask_openapi3 import OpenAPI, Info
from flask_cors import CORS
from flask import redirect
from urllib.parse import unquote


def create_app(config_object=DevConfig):
    """Creates the server

    Args:
        config_object (object, optional): Defaults to DevConfig.
            Adds a config when creating the app server

    Returns:
        class 'flask.app.Flask': A Flask app
    """

    info = Info(title="Minha API", version="1.0.0")
    app = OpenAPI(__name__, info=info)
    CORS(app)

    app.register_api(arxiv_document.blueprint)
    app.register_api(home.blueprint)

    return app
