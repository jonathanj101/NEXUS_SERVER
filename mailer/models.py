from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
from django.db import models


class EmailLog(models.Model):
    to = models.TextField()  # comma-separated list
    subject = models.CharField(max_length=255)
    template = models.CharField(max_length=255, blank=True)
    provider = models.CharField(max_length=64)
    status = models.CharField(max_length=32, default="queued")  # queued|sent|failed
    message_id = models.CharField(max_length=255, blank=True)
    error = models.TextField(blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    sent_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
