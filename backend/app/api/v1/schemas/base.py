from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True, frozen=True)


class IDModelMixin(BaseModel):
    model_config = ConfigDict(frozen=True)
    id: UUID


class TimestampMixin(BaseModel):
    model_config = ConfigDict(frozen=True)
    created_at: datetime
    updated_at: datetime
