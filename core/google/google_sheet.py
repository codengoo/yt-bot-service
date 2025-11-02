__all__ = ['get_sheet', 'get_sheet_data']

from googleapiclient.discovery import build
from typing import List, Any

from core.google.google_api import credentials


def get_sheet():
    service = build('sheets', 'v4', credentials=credentials)
    sheet = service.spreadsheets()
    return sheet


def get_sheet_data(sheet_id: str, range_name: str):
    sheet = get_sheet()
    result = sheet.values().get(spreadsheetId=sheet_id,
                                range=range_name).execute()
    values = result.get('values', [])
    return values

def get_sheet_data_as_struct(sheet_id: str, range_name: str):
    values = get_sheet_data(sheet_id, range_name)

    headers = values[0]
    data_rows = values[1:]

    structured_data = []
    for row in data_rows:
        # Đảm bảo mỗi dòng có đủ cột (nếu thiếu thì fill bằng None)
        row_data = {
            headers[i]: (row[i] if i < len(row) and row[i] != '' else None)
            for i in range(len(headers))
        }
        structured_data.append(row_data)

    return structured_data

def get_sheet_header(sheet_id: str, range_name: str):
    sheet = get_sheet()
    existing_resp = sheet.values().get(
        spreadsheetId=sheet_id,
        range=range_name,
        majorDimension='ROWS'
    ).execute()
    values = existing_resp.get('values', [])
    headers = values[0] if values else []
    return headers

def push_sheet_data(sheet_id:str, range_name: str, values: List[List[Any]]):
    sheet = get_sheet()

    body = {
        'values': values
    }

    result = sheet.values().append(
        spreadsheetId=sheet_id,
        range=range_name,
        valueInputOption='RAW',
        insertDataOption='INSERT_ROWS',
        body=body
    ).execute()

    return result

def push_sheet_data_as_struct(sheet_id: str, range_name: str, data: List[dict]):
    if not data:
        raise ValueError("Dữ liệu đầu vào trống")

    headers = get_sheet_header(sheet_id, range_name)
    values = [
        [row.get(header, None) for header in headers]
        for row in data
    ]

    push_sheet_data(sheet_id, range_name, values)
