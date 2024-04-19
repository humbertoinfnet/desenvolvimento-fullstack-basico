from pydantic import BaseModel, Field


class ResponseNotFound(BaseModel):
    message: str = Field("Resource not found!", description="Exception Information")