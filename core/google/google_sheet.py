__all__ = ['get_sheet', 'get_sheet_data']

from googleapiclient.discovery import build

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
