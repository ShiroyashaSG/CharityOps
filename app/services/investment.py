from typing import Union
from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject, Donation
from app.crud.donation import donation_crud
from app.crud.charity_project import charity_project_crud


async def invest_funds(
        projects: list[CharityProject], donations: list[Donation]
):
    """Распределяет средства из пожертвований между проектами, инвестируя
    доступные средства.
    """
    for donation in donations:
        if donation.fully_invested:
            continue

        for project in projects:
            if project.fully_invested:
                continue

            amount_to_invest = min(
                donation.full_amount - donation.invested_amount,
                project.full_amount - project.invested_amount
            )

            donation.invested_amount += amount_to_invest
            project.invested_amount += amount_to_invest

            if donation.invested_amount == donation.full_amount:
                donation.fully_invested = True
                donation.close_date = datetime.now(timezone.utc)

            if project.invested_amount == project.full_amount:
                project.fully_invested = True
                project.close_date = datetime.now(timezone.utc)

            if donation.fully_invested:
                break  # Переходим к следующему пожертвованию


async def invest_new_project_or_new_donation(
        session: AsyncSession, obj: Union[CharityProject, Donation]
):
    """Если передан проект — находит все неинвестированные пожертвования
    и инвестирует в него. Если передано пожертвование — находит все
    неинвестированные проекты и инвестирует в них."""
    if isinstance(obj, CharityProject):
        paired_objects = await donation_crud.get_uninvested_donation(session)
        await invest_funds([obj], paired_objects)
    else:
        paired_objects = await charity_project_crud.get_uninvested_project(
            session
        )
        await invest_funds(paired_objects, [obj])
    await session.commit()
    await session.refresh(obj)
    return obj


async def invest_after_update(session: AsyncSession, project: CharityProject):
    """Проверяет статус инвестирования проекта после его обновления и
    обновляет статус, если проект полностью инвестирован, иначе запускается
    процесс инвестирования средств в этот проект."""
    if project.full_amount == project.invested_amount:
        project.fully_invested = True
        project.close_date = datetime.now(timezone.utc)
        await session.commit()
        await session.refresh(project)
    else:
        project = await invest_new_project_or_new_donation(session, project)
    return project
