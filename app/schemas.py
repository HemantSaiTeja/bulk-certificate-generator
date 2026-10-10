
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class RecipientInput(BaseModel):
    name: str = Field(min_length=1, max_length=150)
    email: EmailStr
    certificate_title: str = Field(min_length=1, max_length=200)


class GenerationRequest(BaseModel):
    recipients: list[RecipientInput] = Field(min_length=1, max_length=500)


class RecipientResult(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: str
    status: str
    error_message: str | None = None


class JobResult(BaseModel):
    id: int
    status: str
    total_recipients: int
    successful_count: int
    failed_count: int
