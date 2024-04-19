from pydantic import BaseModel, Field


class ResponseSuccess(BaseModel):
    message: str = Field("mensagem de sucesso", description="Mensagem do response")
    data: dict = Field(description="Dados do retorno da rota")
