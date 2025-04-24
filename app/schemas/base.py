from typing import Optional
from datetime import datetime

from pydantic import BaseModel


class BaseSchemas(BaseModel):
    """Базовая схема для проектов и пожертвований."""
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]
