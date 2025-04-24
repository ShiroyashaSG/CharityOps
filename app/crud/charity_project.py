from typing import Optional
from datetime import timedelta

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject


class CRUDCharityProject(CRUDBase):

    async def get_project_id_by_name(
            self,
            project_name: str,
            session: AsyncSession,
    ) -> Optional[int]:
        """Получение объекта проeкта по полю name."""
        db_project_id = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == project_name
            )
        )
        db_project_id = db_project_id.scalars().first()
        return db_project_id

    async def get_uninvested_project(
            self,
            session: AsyncSession
    ):
        """Получение всех неинвестированных проектов,
        отсортированных по дате создания."""
        projects = select(CharityProject).where(
            CharityProject.fully_invested.is_(False)
        ).order_by(CharityProject.create_date)
        projects = await session.execute(projects)
        projects = projects.scalars().all()
        return projects

    async def get_projects_by_completion_rate(
            self,
            session: AsyncSession
    ):
        """Получение всех закрытых проектов отсортированных по периоду
        сбора средств."""
        projects = (
            select(
                CharityProject,
                (
                    func.julianday(CharityProject.close_date) -
                    func.julianday(CharityProject.create_date)
                ).label("collection_duration")
            ).where(CharityProject.close_date.is_not(None)).order_by(
                "collection_duration"
            )
        )

        projects = await session.execute(projects)
        projects = projects.all()
        formatted_projects = []
        for project, duration_in_days in projects:
            days = int(duration_in_days)
            remainder = duration_in_days - days
            duration_seconds = remainder * 24 * 60 * 60
            time_delta = timedelta(seconds=duration_seconds)
            formatted_duration = (
                f"{days} day{'' if days == 1 else 's'}, {str(time_delta)}"
            )

            formatted_projects.append({
                "name": project.name,
                "duration": formatted_duration,
                "description": project.description
            })

        return formatted_projects


charity_project_crud = CRUDCharityProject(CharityProject)
