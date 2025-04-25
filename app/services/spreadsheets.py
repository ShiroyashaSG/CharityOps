from datetime import datetime


def get_spreadsheet_body(date_time: datetime) -> dict[dict]:
    """Генерирует тело для создания отчёта в виде структуры данных,
    соответствующей формату Google Sheets API."""
    return {
        'properties': {
            'title': f'Отчёт на {date_time}',
            'locale': 'ru_RU'
        },
        'sheets': [
            {
                'properties': {
                    'sheetType': 'GRID',
                    'sheetId': 0,
                    'title': 'Лист1',
                    'gridProperties': {
                        'rowCount': 100,
                        'columnCount': 11
                    }
                }
            }
        ]
    }


def get_spreadsheet_headers(date_time: datetime) -> dict[dict]:
    """Генерирует headers для создания отчёта в виде структуры данных,
    соответствующей формату Google Sheets API."""
    return [
        ['Отчёт от', date_time],
        ['Топ проектов по скорости закрытия'],
        ['Название проекта', 'Время сбора', 'Описание']
    ]


def get_spreadsheet_range(table_values: list[list]) -> str:
    """Вычисляет диапазон ячеек в таблице Google Sheets,
    исходя из количества строк и колонок в данных."""
    num_rows = len(table_values)
    num_columns = max(len(row) for row in table_values)
    return f"A1:{chr(65 + num_columns - 1)}{num_rows}"
