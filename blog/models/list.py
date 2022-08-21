from django.db import models
from blog.models.base import BlogBaseModel


class List(BlogBaseModel):
    name = models.CharField(max_length=250)
    description = models.TextField()

    def __str__(self):
        return self.name
