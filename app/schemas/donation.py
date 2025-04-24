from typing import Optional
from datetime import datetime

from pydantic import BaseModel, PositiveInt, Extra

from .base import BaseSchemas


class DonationBase(BaseModel):
    """Базовая модель пожертвований."""
    comment: Optional[str]
    full_amount: PositiveInt

    class Config:
        extra = Extra.forbid


class DonationCreate(DonationBase):
    """Модель создания пожертвований."""


class DonationAllDB(BaseSchemas, DonationBase):
    """Модель получения списка пожертвований с полными данными.
    Для суперюзера."""
    user_id: Optional[int]

    class Config:
        orm_mode = True


class DonationDB(BaseModel):
    """Модель получения списка пожертвований с частичными данными.
    Для пользователя."""
    id: int
    full_amount: PositiveInt
    comment: Optional[str]
    create_date: datetime

    class Config:
        orm_mode = True
