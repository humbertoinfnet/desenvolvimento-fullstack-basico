from flask import request, Response, current_app, json
from flask_openapi3 import Tag, APIBlueprint

from src.external_interfaces.database.controllers.analyses import Motor
from src.external_interfaces.api.request_data.request_data import RequestData
from src.use_cases.analyses import Runner
from src.interface_adapters.schemas.analyses.analyses import (
    PathAnalyses
)
from src.interface_adapters.schemas.response import (
    ResponseError,
    ResponseSuccess,
    ResponseNoContent
)

tag = Tag(name="Analise", description="Rotas para controle das Analises")
blueprint = APIBlueprint(
    'analises',
    __name__,
    abp_tags=[tag],
    doc_ui=True,
    abp_responses={
        200: ResponseSuccess,
        204: ResponseNoContent,
        500: ResponseError
    }
)


@blueprint.get(
    '/analyses/<string:document>/<string:type_policy>',
    responses={200: ResponseSuccess}
)
def get_analyses(path: PathAnalyses):
    """
    Rota GET para aplicar a politica de crédito a um documento
    """

    current_app.logger.info('[route-layers] - acessa a rota GET /analyses')

    request_data = RequestData(path.document)
    motor = Motor()
    runner = Runner(
        document=path.document,
        type_policy=path.type_policy,
        motor=motor,
        request_data=request_data
    )
    
    data = runner.execute()

    return Response(
        json.dumps(data, ensure_ascii=False),
        mimetype="application/json",
        status=200,
    )
