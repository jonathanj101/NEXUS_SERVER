import base64
from typing import Iterable, List, Optional, Tuple, Dict
from django.conf import settings
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content, Attachment, Category

from .base import AbstractEmailProvider


class SendGridProvider(AbstractEmailProvider):
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or settings.SENDGRID_API_KEY
        self.client = SendGridAPIClient(self.api_key)

    def send(
        self,
        *,
        to: Iterable[str],
        subject: str,
        html_body: str,
        text_body: Optional[str] = None,
        from_email: Optional[str] = None,
        attachments: Optional[List[Tuple[str, bytes, str]]] = None,
        headers: Optional[Dict[str, str]] = None,
        categories: Optional[Iterable[str]] = None,
    ) -> Dict:

        message = Mail(
            from_email=Email(from_email),
            to_emails=[To(addr) for addr in to],
            subject=subject,
            html_content=Content("text/html", html_body),
        )
        if text_body:
            # SendGrid will use html_content; adding text as an additional content part
            message.add_content(Content("text/plain", text_body))

        # categories/tags
        cats = list(categories or []) or getattr(settings, "SENDGRID_CATEGORIES", [])
        for c in cats:
            message.add_category(Category(c))

        # headers
        if headers:
            message.headers = headers

        # attachments
        for filename, content_bytes, mimetype in attachments or []:
            att = Attachment()
            att.file_content = base64.b64encode(content_bytes).decode()
            att.file_type = mimetype
            att.file_name = filename
            att.disposition = "attachment"
            message.add_attachment(att)

        resp = self.client.send(message)
        # message ID is in headers
        sg_msg_id = (
            resp.headers.get("X-Message-Id") or resp.headers.get("X-Message-ID") or ""
        )
        return {
            "provider": "sendgrid",
            "message_id": sg_msg_id,
            "raw": {"status_code": resp.status_code},
        }
