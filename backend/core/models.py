from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


# Create your models here.
class BaseModel(models.Model):
    uuid = models.UUIDField(primary_key=False, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True

    def to_json(self):
        return {"uuid": self.uuid}


class UserModel(AbstractUser, BaseModel):
    bio = models.TextField(max_length=500, blank=True)
    point = models.IntegerField(default=0)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
