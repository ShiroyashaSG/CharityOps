from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Donation, User


class CRUDDonation(CRUDBase):

    async def get_by_user(
            self,
            session: AsyncSession,
            user: User
    ) -> list[Donation]:
        """Получение объектов пожертвований пользователя."""
        donation = select(Donation).where(
            Donation.user_id == user.id
        )
        donation = await session.execute(donation)
        donation = donation.scalars().all()

        return donation

    async def get_uninvested_donation(
            self,
            session: AsyncSession
    ):
        """Получение всех неинвестированных проектов,
        отсортированных по дате создания."""
        projects = select(Donation).where(
            Donation.fully_invested.is_(False)
        ).order_by(Donation.create_date)
        projects = await session.execute(projects)
        projects = projects.scalars().all()
        return projects


donation_crud = CRUDDonation(Donation)
