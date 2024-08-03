from datetime import datetime, timezone

from pydantic import BaseModel, Field


class User(BaseModel):
    first_name: str
    last_name: str


class Content(BaseModel):
    text: str | None = None
    photo: str | None = None


class Message(BaseModel):
    user: User
    content: Content
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc))
