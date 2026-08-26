import base64

import requests

from .. import config
from ..interfaces import IEmailService


class GmailAPI(IEmailService):
    def __init__(self):
        self.GMAIL_API_URL = f"{config.GMAIL_API_BASE_URL}/messages"

    def get_message_content(self, message_id: str, headers: dict) -> str:
        response = requests.get(
            f"{self.GMAIL_API_URL}/{message_id}",
            headers=headers,
            params={"format": "full"},
        )
        if response.status_code == 200:
            msg = response.json()
            payload = msg.get("payload", {})

            text_content = ""
            if "parts" in payload:
                for part in payload["parts"]:
                    if part.get("mimeType") == "text/plain":
                        data = part.get("body", {}).get("data", "")
                        if data:
                            try:
                                text_content += base64.urlsafe_b64decode(data).decode(
                                    "utf-8"
                                )
                            except Exception:
                                pass
            elif payload.get("body", {}).get("data"):
                try:
                    text_content = base64.urlsafe_b64decode(
                        payload["body"]["data"]
                    ).decode("utf-8")
                except Exception:
                    text_content = msg.get("snippet", "")

            return text_content[:500]
        return ""

    def get_messages_list(self, headers: dict, max_results: int = 10) -> dict:
        params = {
            "maxResults": max_results,
            "format": "metadata",
        }

        response = requests.get(self.GMAIL_API_URL, headers=headers, params=params)

        if response.status_code == 200:
            data = response.json()
            messages = data.get("messages", [])

            result = []
            for msg in messages:
                detail_response = requests.get(
                    f"{self.GMAIL_API_URL}/{msg['id']}",
                    headers=headers,
                    params={"format": "full"},
                )
                if detail_response.status_code == 200:
                    msg_detail = detail_response.json()
                    payload = msg_detail.get("payload", {})
                    headers_list = payload.get("headers", [])

                    subject = next(
                        (h["value"] for h in headers_list if h["name"] == "Subject"),
                        "No Subject",
                    )
                    from_email = next(
                        (h["value"] for h in headers_list if h["name"] == "From"),
                        "Unknown",
                    )
                    date = next(
                        (h["value"] for h in headers_list if h["name"] == "Date"),
                        "Unknown",
                    )
                    snippet = msg_detail.get("snippet", "")

                    full_content = self.get_message_content(msg["id"], headers)

                    result.append(
                        {
                            "id": msg["id"],
                            "threadId": msg["threadId"],
                            "subject": subject,
                            "from": from_email,
                            "date": date,
                            "snippet": snippet,
                            "content": full_content,
                        }
                    )

            return {
                "success": True,
                "count": len(result),
                "emails": result,
            }
        else:
            return {
                "success": False,
                "error": f"Gmail API error: {response.status_code}",
                "details": response.text,
            }
