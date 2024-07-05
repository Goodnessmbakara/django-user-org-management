from django.db import models
import uuid

class Organisation(models.Model):
    org_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=100, null=False)
    description = models.TextField(blank=True, null=True)
    users = models.ManyToManyField("user.User", related_name='organisations')

    def __str__(self):
        return self.name
