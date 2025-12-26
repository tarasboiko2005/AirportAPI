from django.db import models
from django.conf import settings

class RoadmapRequest(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="llm_requests",
        null=True, blank=True
    )
    topic = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Request({self.topic}) by {self.user or 'Anonymous'}"

class RoadmapResult(models.Model):
    request = models.OneToOneField(
        RoadmapRequest,
        on_delete=models.CASCADE,
        related_name="result"
    )
    response_json = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Result for {self.request.topic}"