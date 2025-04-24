from datetime import datetime, timezone

from sqlalchemy import Column, Integer, Boolean, DateTime


class BaseMixin:
    """Базовый класс для моделей проектов и пожертвований."""

    __abstract__ = True

    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    close_date = Column(DateTime, nullable=True)
