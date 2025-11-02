from pprint import pprint

from fastapi import APIRouter
from pydantic import BaseModel

from core.config import settings
from services.phat_nguoi import phat_nguoi
from core.google import  google_sheet

router = APIRouter(prefix="/traffic-violation", tags=["violations"])

class TrafficViolationSearch(BaseModel):
    bsx: str

# POST /
@router.post("/")
def check(body: TrafficViolationSearch):
    html_content = phat_nguoi.get_raw_violations(body.bsx, 1, phat_nguoi.get_session())
    violations = phat_nguoi.extract_violations(html_content)
    pprint(violations)
    phat_nguoi.send_violations(violations)

# POST /checklist
@router.post("/checklist")
def check():
    userlist = google_sheet.get_sheet_data_as_struct(settings.SHEET_ID_PHAT_NGUOI, "Sheet1")
    for case in userlist:
        pprint(case)
        html_content = phat_nguoi.get_raw_violations(case["bsx"], 1, phat_nguoi.get_session())
        violations = phat_nguoi.extract_violations(html_content)
        pprint(violations)
        phat_nguoi.send_violations(violations)
