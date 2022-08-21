from ckeditor.fields import RichTextField
from core.managers import ActiveManager
from django.contrib.auth import get_user_model
from django.db import models
from taggit.managers import TaggableManager
from blog.validators import validate_cover
from blog.models.base import BlogBaseModel
from blog.models.category import Category
from blog.models.list import List

User = get_user_model()


class Article(BlogBaseModel):
    """
    NOTE:
        - The author field must be null because of on_delete
    """

    STATUS_CHOICES = (
        ("d", "draft"),
        ("p", "publish"),
    )
    author = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    list = models.ForeignKey(List, blank=True, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique=True)
    description = RichTextField()
    preview = models.CharField(max_length=500, default="")
    cover = models.ImageField(upload_to="media/article/", validators=[validate_cover])
    likes = models.ManyToManyField(User, blank=True, related_name="article_like")
    vpn = models.BooleanField(default=False)

    objects = models.Manager()
    active = ActiveManager()
    tags = TaggableManager()

    class Meta:
        ordering = ["-id"]
        verbose_name = "Article"
        verbose_name_plural = "Articles"

    def __str__(self):
        return self.title

    def likes_count(self):
        return self.likes.count()
