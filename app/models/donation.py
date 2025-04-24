from sqlalchemy import Column, Text, Integer, ForeignKey

from app.core.db import Base
from .base import BaseMixin


class Donation(Base, BaseMixin):
    """Модель пожертвований."""
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text, nullable=True)
