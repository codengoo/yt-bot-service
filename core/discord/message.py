from typing import Optional, Dict, Any


class DiscordMessage:
    def __init__(self, content: str, embed: Optional[Dict[str, Any]] = None):
        self.content = content
        self.embed = embed

    def to_payload(self) -> Dict[str, Any]:
        """
        Chuyển object thành payload JSON để gửi lên Discord API.
        """
        payload = {"content": self.content}
        if self.embed:
            payload["embeds"] = [self.embed]
        return payload