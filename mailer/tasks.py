from celery import shared_task
from typing import Dict, Iterable, List, Optional, Tuple
from .services import send_templated_email

Attachment = Tuple[str, bytes, str]


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, max_retries=5)
def send_templated_email_task(
    *,
    to: Iterable[str],
    subject: str,
    template: str,
    context: Dict,
    from_email: Optional[str] = None,
    attachments: Optional[List[Attachment]] = None,
    headers: Optional[Dict[str, str]] = None,
    categories: Optional[Iterable[str]] = None,
):
    return send_templated_email(
        to=to,
        subject=subject,
        template=template,
        context=context,
        from_email=from_email,
        attachments=attachments,
        headers=headers,
        categories=categories,
    ).id
