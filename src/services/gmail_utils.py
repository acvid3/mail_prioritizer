import requests

def get_message_content(message_id: str, headers: dict, gmail_api_url: str):
    """Get full email content"""
    response = requests.get(f"{gmail_api_url}/{message_id}", headers=headers, params={"format": "full"})
    if response.status_code == 200:
        msg = response.json()
        payload = msg.get('payload', {})
        
        # Extract text from email
        text_content = ""
        if 'parts' in payload:
            for part in payload['parts']:
                if part.get('mimeType') == 'text/plain':
                    data = part.get('body', {}).get('data', '')
                    if data:
                        import base64
                        try:
                            text_content += base64.urlsafe_b64decode(data).decode('utf-8')
                        except:
                            pass
        elif 'body' in payload and payload['body'].get('data'):
            import base64
            try:
                text_content = base64.urlsafe_b64decode(payload['body']['data']).decode('utf-8')
            except:
                text_content = payload.get('snippet', '')
        
        return text_content[:500]  # Limit to 500 characters for display
    return ""
