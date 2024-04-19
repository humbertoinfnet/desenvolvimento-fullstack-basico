from pydantic import BaseModel, Field


class ResponseNoContent(BaseModel):
    message: str = Field(description="Mensagem do response")
