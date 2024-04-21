from flask_openapi3 import OpenAPI, Info
from flask_cors import CORS
from .register_route import register_route


def create_app() -> OpenAPI:
    """
    Criação do servidor flask
    """

    info = Info(title="Minha API", version="1.0.0")
    app = OpenAPI(
        __name__,
        info=info,
    )
    CORS(app)
    return app
