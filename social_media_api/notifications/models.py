from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.conf import settings

class Notification(models.Model):
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='actor_notifications')
    verb = models.CharField(max_length=255)

    target_object_id = models.PositiveIntegerField(null=True, blank=True)
    target_content_type = models.ForeignKey('contenttypes.ContentType', on_delete=models.CASCADE, null=True, blank=True)
    target_object = GenericForeignKey('target_content_type', 'target_object_id')
    read = models.BooleanField(default=False)

    timestamp = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.actor.username} {self.verb} {self.recipient.username}"
    