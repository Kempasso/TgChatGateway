from pydantic import BaseModel, Field


class CreateChatSerializer(BaseModel):
    chat_id: int = Field(alias='id')
    first_name: str
    language: str = Field(alias='language_code')
