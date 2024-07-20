from django.db import models

# Create your models here.
class BaseModel(models.Model):
    """ BaseModel for common database fields."""

    created_at = models.DateTimeField("Created Date", auto_now_add=True)
    updated_at = models.DateTimeField("Updated Date", auto_now=True)

    class Meta:
        abstract = True