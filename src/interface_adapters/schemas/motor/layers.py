from typing import Optional
from pydantic import BaseModel, Field, RootModel


class PathLayer(BaseModel):
    layer_id: int = Field(..., description='Id da camada')


class BodyLayer(BaseModel):
    name: Optional[str] = Field(None, description='Nome da camada')
    description: Optional[str] = Field(None, description='Descrição da camada')


class ResponseLayer(BaseModel):
    layer_id: int = Field(None, description='Id da camada')
    name: str = Field(None, description='Nome da camada')
    description: str = Field(None, description='Descrição da camada')
    identify: str = Field(None, description='Identificacao do elemento')


class ResponseSuccessLayer(RootModel):
    root: list[ResponseLayer] = Field(description="Array dos objetos")


class ResponseSuccessLayerDelete(BaseModel):
    message: str = Field("success_delete_layer", description="Mensagem do response")
    deleted: list[ResponseLayer]


class ResponseSuccessLayerUpdate(BaseModel):
    message: str = Field("success_update_layer", description="Mensagem do response")
    previous: list[ResponseLayer]
    updated: list[ResponseLayer]


class ResponseSuccessLayerAdd(BaseModel):
    message: str = Field("success_add_layer", description="Mensagem do response")
    create: list[ResponseLayer]
