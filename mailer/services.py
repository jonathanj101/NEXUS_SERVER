from typing import Dict, Iterable, List, Optional, Tuple
import smtplib
import logging
from dataclasses import dataclass
from django.conf import settings
from django.template.loader import render_to_string
from django.utils import timezone

from .models import EmailLog
from .providers.base import AbstractEmailProvider
from .providers.django_smtp import DjangoSMTPProvider

# from .providers.sendgrid import SendGridProvider

Attachment = Tuple[str, bytes, str]  # (filename, content_bytes, mimetype)


@dataclass
class EmailTemplateSpec:
    """Convenience wrapper to list template base names without extension."""

    name: str  # e.g. "welcome" -> expects email/welcome.html and email/welcome.txt
    context: Dict


def get_provider() -> AbstractEmailProvider:
    provider = getattr(settings, "EMAIL_PROVIDER", "django").lower()
    # if provider == "sendgrid":
    #     return SendGridProvider()
    # default
    return DjangoSMTPProvider()


def render_email(template_name: str, context: Dict) -> Dict[str, str]:
    """
    Given 'welcome' renders:
      - email/welcome.html  (html_body)
      - email/welcome.txt   (text_body; optional; falls back to stripping tags if missing)
    """
    html_body = render_to_string(f"emails/{template_name}.html", context)
    try:
        text_body = render_to_string(f"emails/{template_name}.txt", context)
    except Exception:
        # optional: a primitive fallback if you prefer
        text_body = None
    return {"html": html_body, "text": text_body}


def send_templated_email(
    # *,
    to: Iterable[str],
    subject: str,
    template: str,
    context: Dict,
    from_email: Optional[str] = None,
    attachments: Optional[List[Attachment]] = None,
    headers: Optional[Dict[str, str]] = None,
    categories: Optional[Iterable[str]] = None,
) -> EmailLog:
    from_email = from_email or settings.DEFAULT_FROM_EMAIL
    provider = get_provider()
    bodies = render_email(template, context)

    log = EmailLog.objects.create(
        to=",".join(to),
        subject=subject,
        template=template,
        provider=provider.__class__.__name__.replace("Provider", "").lower(),
        status="queued",
        metadata={"context_keys": list(context.keys())},
    )
    # print(context["user"])
    try:
        result = provider.send(
            to=to,
            subject=subject,
            from_email=from_email,
            html_body=bodies["html"],
            text_body=bodies["text"],
            attachments=attachments,
            headers=headers,
            categories=categories,
        )
        log.status = "sent"
        log.message_id = result.get("message_id", "")
        log.sent_at = timezone.now()
        log.metadata.update(result.get("raw", {}))
        log.save(update_fields=["status", "message_id", "metadata", "sent_at"])
    # except smtplib.SMTPRecipientsRefused as e:
    #     for addr, (code, msg) in e.recipients.items():
    #         logging.warning(
    #             "RCPT refused: %s -> %s %s",
    #             addr,
    #             code,
    #             msg.decode() if isinstance(msg, bytes) else msg,
    #         )
    #     raise
    except Exception as e:
        log.status = "failed"
        log.error = str(e)
        log.save(update_fields=["status", "error"])
        raise

    return log
