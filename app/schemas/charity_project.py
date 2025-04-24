from typing import Optional
from pydantic import BaseModel, PositiveInt, Extra, Field

from .base import BaseSchemas


class CharityProjectBase(BaseModel):
    """Базовая схема проектов."""
    name: str = Field(..., max_length=100)
    description: str = Field(..., max_length=100)
    full_amount: PositiveInt

    class Config:
        extra = Extra.forbid
        min_anystr_length = 1


class CharityProjectUpdate(CharityProjectBase):
    """Схема для обновления пректов."""
    name: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = Field(None, max_length=100)
    full_amount: Optional[PositiveInt] = Field(None)


class CharityProjectCreate(CharityProjectBase):
    """Схема для создания пректов."""


class CharityProjectDB(BaseSchemas, CharityProjectBase):
    """Схема для получения проктов."""

    class Config:
        orm_mode = True
