from pydantic import BaseModel, Field


class ResponseError(BaseModel):
    message: str = Field('mensagem de erro', description="Mensagem de erro")
    error: str = Field('descricao do erro', description="Descricao do erro")
