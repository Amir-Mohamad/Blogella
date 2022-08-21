from django.db import models
from django.contrib.auth import get_user_model
from blog.models import Category
from ckeditor.fields import RichTextField
from blog.validators import validate_cover
from core.managers import ActiveManager
from taggit.managers import TaggableManager
import random
import uuid

User = get_user_model()


class BookBaseModel(models.Model):
    updated = models.DateTimeField(auto_now_add=True)
    created = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False)

    class Meta:
        abstract = True


class Book(BookBaseModel):
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="books"
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="books"
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(unique=True)
    content = RichTextField()
    cover = models.ImageField(upload_to="media/book/", validators=[validate_cover])
    link = models.URLField()

    objects = models.Manager()
    active = ActiveManager()
    tags = TaggableManager()

    def __str__(self):
        return self.title
