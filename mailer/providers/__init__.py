from abc import ABC, abstractmethod
from typing import List, Optional, Iterable, Tuple, Dict

Attachment = Tuple[str, bytes, str]  # (filename, content_bytes, mimetype)


class AbstractEmailProvider(ABC):
    @abstractmethod
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
        """
        Returns dict including at least:
          { "provider": ..., "message_id": "...", "raw": {...} }
        """
        raise NotImplementedError
