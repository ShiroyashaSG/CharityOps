from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_full_amount_not_less_than_invested_amount,
    check_project_before_edit,
    check_name_duplicate,
)
from app.core.db import get_async_session
from app.crud.charity_project import charity_project_crud
from app.schemas.charity_project import (
    CharityProjectCreate, CharityProjectDB, CharityProjectUpdate
)
from app.core.user import current_superuser
from app.services.investment import (
    invest_new_project_or_new_donation, invest_after_update
)

router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def create_charity_project(
        charity_project: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров.
    Создание проекта для пожертвований."""
    await check_name_duplicate(charity_project.name, session)
    new_charity_project = await charity_project_crud.create(
        charity_project, session
    )
    invested_project = await invest_new_project_or_new_donation(
        session, new_charity_project
    )
    return invested_project


@router.get(
    '/',
    response_model=list[CharityProjectDB],
)
async def get_all_projects(
        session: AsyncSession = Depends(get_async_session),
):
    """Получает список всех проектов."""
    all_projects = await charity_project_crud.get_multi(session)
    return all_projects


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def delete_project(
        project_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров.
    Удаление проекта для пожертвований."""
    charity_project = await check_project_before_edit(
        project_id, session, check_before_delete=True
    )
    charity_project = await charity_project_crud.remove(
        charity_project, session
    )
    return charity_project


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def update_project(
        project_id: int,
        obj_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров.
    Обновление проекта для пожертвований."""
    project = await check_project_before_edit(project_id, session)

    if obj_in.name is not None:
        await check_name_duplicate(obj_in.name, session)

    if obj_in.full_amount is not None:
        check_full_amount_not_less_than_invested_amount(obj_in, project)
    project = await charity_project_crud.update(
        db_obj=project,
        obj_in=obj_in,
        session=session,
    )
    invested_project = await invest_after_update(session, project)
    return invested_project
