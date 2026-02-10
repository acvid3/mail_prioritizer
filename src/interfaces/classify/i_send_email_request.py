class ISendEmailRequest:
    to: str
    subject: str
    content: str
    thread_id: str = None
