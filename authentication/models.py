from django.db import models
from django.contrib.auth.models import User
import uuid
from django.utils import timezone


class AuthCode(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.UUIDField(default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    expiration_time = models.DateTimeField()
    expired = models.BooleanField(default=False)
    is_used = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # Set expiration_time to current time + 5 minutes

        self.expiration_time = timezone.now() + timezone.timedelta(minutes=5)
        super().save(*args, **kwargs)
