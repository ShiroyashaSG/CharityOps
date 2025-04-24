from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models import CharityProject
from app.schemas.charity_project import CharityProjectUpdate


async def check_name_duplicate(
        project_name: str,
        session: AsyncSession,
) -> None:
    """Проверяет поле name на уникальность."""
    project_id = await charity_project_crud.get_project_id_by_name(
        project_name, session
    )
    if project_id is not None:
        raise HTTPException(
            status_code=400,
            detail='Проект с таким именем уже существует!',
        )


async def check_project_before_edit(
        project_id: int,
        session: AsyncSession,
        check_before_delete: bool = False
) -> CharityProject:
    """Проверяет, что изменяемый проект существует, запрещяает изменять проект,
    если он закрыт и удалять его, если в него уже внесли пожертвования."""
    charity_project = await charity_project_crud.get(project_id, session)
    if charity_project is None:
        raise HTTPException(
            status_code=404,
            detail='Проект не найден!'
        )
    if check_before_delete and charity_project.invested_amount > 0:
        raise HTTPException(
            status_code=400,
            detail='Нельзя удалять проект, с инвистированными стредствами!'
        )
    if charity_project.fully_invested:
        raise HTTPException(
            status_code=400,
            detail='Нельзя удалять или изменять закрытый проект!'
        )
    return charity_project


def check_full_amount_not_less_than_invested_amount(
    obj_in: CharityProjectUpdate,
    project: CharityProject,
) -> None:
    """Проверяет, что поле full_amount должно быть больше invested_amount."""
    if obj_in.full_amount < project.invested_amount:
        raise HTTPException(
            status_code=400,
            detail="Поле full_amount не может быть меньше уже внесенной суммы"
        )
