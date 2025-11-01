__all__ = ["credentials"]

from google.oauth2 import service_account

SERVICE_ACCOUNT_FILE = 'service-account.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# Tạo credentials từ service account
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)
