from flask import json, current_app, Response
from flask_openapi3 import APIBlueprint


blueprint = APIBlueprint('errorhandler', __name__)

@blueprint.app_errorhandler(Exception)
def handle_exception(err):
    """Return JSON instead of HTML for HTTP errors."""
    current_app.logger.error(f'[handle_exception] - problema - Error: {err}')
    return Response(
        json.dumps({"message": "internal_server_error", "error": str(err)}, ensure_ascii=False),
        mimetype="application/json",
        status=500,
    )
