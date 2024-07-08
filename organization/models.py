from django.db import models

class Organisation(models.Model):
    orgId = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=False)
    description = models.TextField(blank=True, null=True)
    users = models.ManyToManyField("user.User", related_name='organisations')

    def __str__(self):
        return self.name
