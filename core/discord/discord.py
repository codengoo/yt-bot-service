import requests

from core.config import settings
from core.discord.message import DiscordMessage


def send_message(message: DiscordMessage, channel_id: str):
    bot_token = settings.DISCORD_BOT_TOKEN
    url = f"https://discord.com/api/v10/channels/{channel_id}/messages"
    headers = {
        "Authorization": f"Bot {bot_token}",
        "Content-Type": "application/json"
    }

    payload = message.to_payload()

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        response.raise_for_status()
        print("✅ Gửi tin nhắn thành công!")
    except requests.RequestException as e:
        print(f"❌ Lỗi khi gửi tin nhắn: {e}")
        if response is not None:
            print(f"Status code: {response.status_code}")
            print(f"Response: {response.text}")
