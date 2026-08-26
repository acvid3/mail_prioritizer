import base64

import requests

from .. import config


def verify_google_token(access_token: str) -> bool:
    try:
        response = requests.get(
            config.GOOGLE_USERINFO_URL,
            headers={"Authorization": f"Bearer {access_token}"},
        )
        return response.status_code == 200
    except requests.RequestException:
        return False


def get_message_content(message_id: str, headers: dict) -> str:
    gmail_api_url = f"{config.GMAIL_API_BASE_URL}/messages"
    response = requests.get(
        f"{gmail_api_url}/{message_id}",
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
                text_content = payload.get("snippet", "")

        return text_content[:500]
    return ""
