from django.db import models
from django.contrib.auth import get_user_model
from blog.models import Article
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from .managers import ActiveManager

User = get_user_model()


class CoreBaseModel(models.Model):
    updated = models.DateTimeField(auto_now_add=True)
    created = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False)

    class Meta:
        abstract = True


class Comment(CoreBaseModel):
    """
    The main comment model in article and blog pages
    """

    ARTICLE = "article"
    BOOK = "book"
    TYPE_CHOICES = (
        (ARTICLE, "Article"),
        (BOOK, "Book"),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    # article = models.ForeignKey(
    #     Article, on_delete=models.CASCADE, related_name='comments', null=True, blank=True)
    body = models.CharField(max_length=400, default="")

    parent_object_id = models.IntegerField(default=1)
    parent_content_type = models.ForeignKey(
        ContentType,
        on_delete=models.PROTECT,
    )
    parent = GenericForeignKey(
        "parent_content_type",
        "parent_object_id",
    )

    objects = models.Manager()
    active = ActiveManager()

    def is_comment_active(self):
        if self.is_active:
            return True
        else:
            return False

    is_comment_active.boolean = True

    def __str__(self):
        return self.body[:20]


class Reply(CoreBaseModel):
    """
    Used for making replies on comments in articles and blogs
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="replies")
    comment = models.ForeignKey(
        Comment, on_delete=models.CASCADE, related_name="replies"
    )
    body = models.TextField(max_length=400)

    def __str__(self):
        return self.body
