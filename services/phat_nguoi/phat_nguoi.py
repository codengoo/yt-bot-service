from datetime import datetime
from typing import List

import requests
from bs4 import BeautifulSoup

from core.config import settings
from core.discord.discord import send_message
from core.discord.message import DiscordMessage
from services.phat_nguoi.traffic_violation import TrafficViolation


def get_raw_violations(bien_so: str, loai_xe: int, session_id: str) -> str:
    url = f"https://phatnguoixe.com/102699"

    data = {
        "BienSo": bien_so,
        "LoaiXe": loai_xe
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Cookie": f"PHPSESSID={session_id};"
    }

    try:
        response = requests.post(url, data=data, headers=headers, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Lỗi khi gửi request: {e}")
        return ""


def get_session():
    url = "https://phatnguoixe.com/"
    session = requests.Session()

    try:
        response = session.get(url, timeout=10)
        response.raise_for_status()

        # Lấy cookie PHPSESSID từ session
        phpsessid = session.cookies.get("PHPSESSID")
        if phpsessid:
            return phpsessid
        else:
            return ""
    except requests.RequestException as e:
        print(f"Lỗi khi gửi request: {e}")
        return ""


def extract_violations(raw_violations: str) -> List[TrafficViolation]:
    soup = BeautifulSoup(raw_violations, "html.parser")
    violations = []

    for table_div in soup.select("div.body_table"):
        item = {}
        rows = table_div.select("tr.td_left")

        for row in rows:
            cells = row.find_all("td")
            if len(cells) >= 2:
                key = cells[0].get_text(strip=True).replace(":", "")
                value = cells[1].get_text(strip=True)
                item[key] = value

        if item:
            # Map từ key tiếng Việt sang field dataclass
            try:
                violation = TrafficViolation(
                    license_plate=item.get("Biển số", ""),
                    vehicle_type=item.get("Loại phương tiện", ""),
                    violation_time=datetime.strptime(item.get("Thời gian vi phạm", ""), "%H:%M, %d/%m/%Y"),
                    violation_location=item.get("Địa điểm vi phạm", ""),
                    violation_action=item.get("Hành vi vi phạm", ""),
                    status=item.get("Trạng thái", "")
                )
                violations.append(violation)
            except Exception as e:
                print(f"Error parsing violation: {e}, item: {item}")

    return violations


def send_violations(violations: List[TrafficViolation]):
    for violation in violations:
        test_embed = {
            "title": f"🌸 Phát hiện vi phạm - {violation.license_plate}",
            "color": 15277667,
            "description": violation.violation_action,
            "fields": [
                {
                    "name": "Loại xe",
                    "value": violation.vehicle_type,
                    "inline": True
                },
                {
                    "name": "Thời gian",
                    "value": violation.violation_time.strftime("%H:%M, %d/%m/%Y"),
                    "inline": True
                },
                {
                    "name": "Địa điểm vi phạm",
                    "value": violation.violation_location
                },
                {
                    "name": "Trạng thái",
                    "value": violation.status
                }
            ]
        }

        message = DiscordMessage(
            content="🚨 Phát hiện vi phạm mới!",
            embed=test_embed
        )

        send_message(message=message, channel_id=settings.DISCORD_CHANNEL_PHAT_NGUOI)
