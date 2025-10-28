from typing import Iterable, List, Optional, Tuple, Dict
from django.core.mail import EmailMultiAlternatives
from .base import AbstractEmailProvider, Attachment


class DjangoSMTPProvider(AbstractEmailProvider):
    def send(
        self,
        *,
        to: Iterable[str],
        subject: str,
        html_body: str,
        text_body: Optional[str] = None,
        from_email: Optional[str] = None,
        attachments: Optional[List[Attachment]] = None,
        headers: Optional[Dict[str, str]] = None,
        categories: Optional[Iterable[str]] = None,
    ) -> Dict:
        msg = EmailMultiAlternatives(
            subject=subject,
            body=text_body or "",
            from_email=from_email,
            to=list(to),
            headers=headers or {},
        )
        msg.attach_alternative(html_body, "text/html")
        for att in attachments or []:
            filename, content, mimetype = att
            msg.attach(filename, content, mimetype)
        message_id = msg.send(fail_silently=False)
        # Django returns number of successfully delivered messages, not a true id
        return {"provider": "django", "message_id": str(message_id), "raw": {}}
