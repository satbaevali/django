from django.db import models
from typing import Any

from django.utils import timezone as django_timezone

class AbstractBaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True,null=True)
    
    class Meta:
        abstract = True
        
    def delete(self, *args: tuple[Any, ...], **kwargs: dict[Any, Any])->None:
        self.deleted_at = django_timezone.now()
        self.save(update_fields=["deleted_at"])
