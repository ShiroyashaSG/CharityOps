from datetime import datetime

from aiogoogle import Aiogoogle
from app.core.config import settings
from .spreadsheets import (
    get_spreadsheet_body,
    get_spreadsheet_headers,
    get_spreadsheet_range
)

# Константа с форматом строкового представления времени
FORMAT = "%Y/%m/%d %H:%M:%S"


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    # Получаем текущую дату для заголовка документа
    now_date_time = datetime.now().strftime(FORMAT)
    # Создаём экземпляр класса Resource
    service = await wrapper_services.discover('sheets', 'v4')
    # Формируем тело запроса
    spreadsheet_body = get_spreadsheet_body(now_date_time)
    # Выполняем запрос
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    spreadsheet_id = response['spreadsheetId']
    return spreadsheet_id


async def set_user_permissions(
        spreadsheet_id: str,
        wrapper_services: Aiogoogle
) -> None:
    permissions_body = {'type': 'user',
                        'role': 'writer',
                        'emailAddress': settings.email}
    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheet_id,
            json=permissions_body,
            fields="id"
        ))


async def spreadsheets_update_value(
        spreadsheet_id: str,
        charity_projects: list,
        wrapper_services: Aiogoogle
) -> None:
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')
    spreadsheet_headers = get_spreadsheet_headers(now_date_time)
    table_values = [
        *spreadsheet_headers,
        *[
            list(map(str, [
                project['name'],
                project['duration'],
                project['description']
            ]))
            for project in charity_projects
        ]
    ]

    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }

    spreadsheet_range = get_spreadsheet_range(table_values)

    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range=spreadsheet_range,
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )
