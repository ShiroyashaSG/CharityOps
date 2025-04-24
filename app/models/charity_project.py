from sqlalchemy import Column, String, Text

from app.core.db import Base
from .base import BaseMixin


class CharityProject(Base, BaseMixin):
    """Модель проектов."""
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)
