from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User
from app.core.user import current_user
from app.core.db import get_async_session
from app.crud.donation import donation_crud
from app.schemas.donation import (
    DonationCreate, DonationDB, DonationAllDB
)
from app.core.user import current_superuser, current_user
from app.services.investment import invest_new_project_or_new_donation

router = APIRouter()


@router.post(
    '/',
    response_model=DonationDB
)
async def create_donation(
        donation: DonationCreate,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    """Создание пожертвования."""
    new_donation = await donation_crud.create(
        donation, session, user
    )
    invested_donation = await invest_new_project_or_new_donation(
        session, new_donation
    )
    return invested_donation


@router.get(
    '/',
    response_model=list[DonationAllDB],
    dependencies=[Depends(current_superuser)],
)
async def get_all_donations(
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров.
    Получает список всех пожертвований.
    """
    all_donations = await donation_crud.get_multi(session)
    return all_donations


@router.get(
    '/my',
    response_model=list[DonationDB],
    response_model_exclude={'user_id'},
)
async def get_my_donations(
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    """Получает список всех пожертвований для текущего пользователя."""
    donations = await donation_crud.get_by_user(
        session=session, user=user
    )
    return donations
