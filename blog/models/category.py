from core.managers import ActiveManager
from django.contrib.auth import get_user_model
from django.db import models
from blog.models.base import BlogBaseModel

User = get_user_model()


class Category(BlogBaseModel):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    objects = models.Manager()
    active = ActiveManager()

    class Meta:
        verbose_name = "Article Category"
        verbose_name_plural = "Article Categories"

    def __str__(self):
        return self.name
