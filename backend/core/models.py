from logging import warn
from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

from django.http import HttpRequest, QueryDict


# Create your models here.
class BaseModel(models.Model):
    uuid = models.UUIDField(primary_key=False, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True

    def to_json(self, **kwargs):
        return self.sample_to_json(**kwargs)

    def loop_all_self_attr(
        self, with_foreign=True, with_related=False, related_serializer=False
    ):
        """遍历所有属性

        Returns:
            _type_: _description_
        """
        for key in self.__dict__:
            if hasattr(self, key):
                if key == "_state":
                    continue
                yield key, getattr(self, key)

        for fKey in self.foreignKeys():
            if hasattr(self, fKey.name) and with_foreign is True:
                foreign = getattr(self, fKey.name)
                if hasattr(foreign, "to_json"):
                    yield fKey.name, getattr(self, fKey.name).to_json()
            # related
            if fKey.related_model is not None and with_related is True:
                related = fKey.related_model
                # print(self.__class__.__name__, fKey.name, related.__class__.__name__)
                arr = []
                if hasattr(related, self.__class__.__name__.lower()) is False:
                    continue

                for item in related.objects.filter(
                    **{self.__class__.__name__.lower(): self}
                ).all():
                    if item is not None and hasattr(item, "to_json"):
                        if related_serializer is True:
                            arr.append(
                                item.to_json(  # type: ignore
                                    with_foreign=False,
                                    related_serializer=False,
                                    with_related=False,
                                )  # type: ignore
                            )
                            continue
                        arr.append(item.__str__())
                yield fKey.name, arr
                yield fKey.name + "_count", len(arr)

    def extra_json(self):
        return {}

    def foreignKeys(self):
        return [f for f in self._meta.get_fields() if f.is_relation]

    def sample_to_json(
        self,
        with_foreign=True,
        with_related=True,
        related_serializer=False,
        merge_force=False,
    ):
        """转换为json

        Returns:
            _type_: _description_
        """
        result = {
            key: value
            for key, value in self.loop_all_self_attr(
                with_foreign=with_foreign,
                with_related=with_related,
                related_serializer=related_serializer,
            )
        }

        for key, value in self.extra_json().items():
            if merge_force is True:
                result[key] = value
            else:
                if result.get(key) is None:
                    result[key] = value
                else:
                    warn("key %s is exists" % key)

        return result


class UserModel(AbstractUser, BaseModel):
    bio = models.TextField(max_length=500, blank=True)
    point = models.IntegerField(default=0)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
