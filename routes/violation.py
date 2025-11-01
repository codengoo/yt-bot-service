from pprint import pprint

from fastapi import APIRouter
from pydantic import BaseModel
from services.phat_nguoi import phat_nguoi

router = APIRouter(prefix="/traffic-violation", tags=["violations"])

class TrafficViolationSearch(BaseModel):
    bsx: str

# POST /
@router.post("/")
def check(body: TrafficViolationSearch):
    html_content = phat_nguoi.get_raw_violations(body.bsx, 1, "e4be203184dd60ef22c2ffddb70c278e")
    # print(html_content[:500])
    violations = phat_nguoi.extract_violations(html_content)
    pprint(violations)
    phat_nguoi.send_violations(violations)
