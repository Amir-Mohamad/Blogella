from django.urls import path, include
from rest_framework import routers
from . import views


app_name = 'blog'

urlpatterns = [
    # articles
    path('articles/', views.ArticleListView.as_view(), name="list"),

    path('article/<str:slug>', views.ArticleRetrieveView.as_view(), name="detail"),

    # comments
    path('comments/<int:pk>/', views.CommentListView.as_view(),
         name="comment-per-article"),
    path('comment/create/<str:type>/<int:parent_id>/',
         views.CommentCreate.as_view(), name="article-create-comment"),
    path('comment/update/<str:type>/<int:parent_id>/<int:comment_id>/',
         views.CommentUpdate.as_view(), name="article-update-comment"),
    path('comment/delete/<str:type>/<int:parent_id>/<int:comment_id>/',
         views.CommentDelete.as_view(), name="article-delete-comment"),

    # like
    path('article/like/<int:article_id>/',
         views.ArticleLike.as_view(), name="article_like"),

    # replies
    path('reply/create/<int:comment_id>/',
         views.ReplyCreate.as_view(), name="reply-create"),
    path('reply/update/<int:comment_id>/<int:reply_id>/',
         views.ReplyUpdate.as_view(), name="reply-update"),
    path('reply/delete/<int:comment_id>/<int:reply_id>/',
         views.ReplyDelete.as_view(), name="reply-delete"),
    path('reply/<int:pk>/', views.ReplyListView.as_view(), name="comment-replies")
]
