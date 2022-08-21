from blog.models import Article
from core.models import Comment, Reply
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.generics import ListAPIView, RetrieveAPIView
from utilities.pagination import StandardResultsSetPagination
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from utilities.permissions import IsOwnerOrReadOnly, ReadOnly
from .serializers import CommentSerializer
from .serializers import ReplySerializer, CommentSerializer, ArticleSerializer
from django.contrib.contenttypes.models import ContentType
from book.models import Book


class BasicPagination:
    pass


class PaginationHandlerMixin:
    pass


class ArticleListView(ListAPIView):
    queryset = Article.active.all()
    pagination_class = StandardResultsSetPagination
    serializer_class = ArticleSerializer

    def get_serializer(self, *args, **kwargs):
        serializer = self.serializer_class(
            self.get_queryset(), many=True, remove_fields=["created", "description"]
        )
        return serializer


class ArticleRetrieveView(RetrieveAPIView):
    queryset = Article.active.all()
    pagination_class = StandardResultsSetPagination
    serializer_class = ArticleSerializer
    lookup_field = "slug"


# TODO: Refactor comment and reply views (we are using M2M and thats wrong)


class CommentListView(ListAPIView):
    permission_classes = [ReadOnly]
    serializer_class = CommentSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        queryset = Comment.active.filter(article__id=self.kwargs["pk"])

        return queryset


class CommentCreate(APIView):
    permission_classes = [
        IsAuthenticated,
    ]
    serializer_class = CommentSerializer

    def post(self, request, type, parent_id):
        # default parent
        parent = get_object_or_404(Article, id=parent_id)

        if type == "article":
            parent = get_object_or_404(Article, id=parent_id)
        elif type == "book":
            parent = get_object_or_404(Book, id=parent_id)

        parent_content_type = ContentType.objects.get_for_model(parent)

        body = request.POST.get("body")
        Comment.objects.create(
            user=request.user,
            parent_object_id=parent.id,
            body=body,
            parent_content_type=parent_content_type,
        )
        # serializer = self.serializer_class(
        #     queryset, partial=True, context={'request': request})
        return Response(status=status.HTTP_201_CREATED)


class CommentUpdate(APIView):
    permission_classes = [
        IsOwnerOrReadOnly,
    ]
    serializer_class = CommentSerializer

    def patch(self, request, type, parent_id, comment_id):
        # default parent
        parent = get_object_or_404(Article, id=parent_id)

        if type == "article":
            parent = get_object_or_404(Article, id=parent_id)
        elif type == "book":
            parent = get_object_or_404(Book, id=parent_id)

        parent_content_type = ContentType.objects.get_for_model(parent)

        comment = get_object_or_404(
            Comment,
            pk=comment_id,
            parent_content_type=parent_content_type,
            parent_object_id=parent_id,
        )
        self.check_object_permissions(request, comment)

        serializer = self.serializer_class(
            instance=comment,
            data=request.data,
            partial=True,
            context={"request": request},
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentDelete(APIView):
    permission_classes = [
        IsOwnerOrReadOnly,
    ]

    def delete(self, request, type, parent_id, comment_id):
        parent = get_object_or_404(Article, id=parent_id)
        if type == "article":
            parent = get_object_or_404(Article, id=parent_id)
        elif type == "book":
            parent = get_object_or_404(Book, id=parent_id)

        parent_content_type = ContentType.objects.get_for_model(parent)
        comment = get_object_or_404(
            Comment,
            pk=comment_id,
            parent_content_type=parent_content_type,
            parent_object_id=parent_id,
        )

        self.check_object_permissions(request, comment)

        comment.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class ReplyListView(ListAPIView):
    """
    Shows all replies related to single comment
    """

    permission_classes = [ReadOnly]
    serializer_class = ReplySerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        queryset = Reply.objects.filter(comment__id=self.kwargs["pk"])

        return queryset


class ReplyCreate(APIView):
    permission_classes = [
        IsAuthenticated,
    ]
    serializer_class = ReplySerializer

    def post(self, request, comment_id):

        comment = get_object_or_404(Comment, id=comment_id)

        serializer = self.serializer_class(data={"comment": comment, "user": request.user, "body": request.POST["body"]})  # type: ignore
        if serializer.is_valid():
            serializer.save(user=request.user, comment=comment)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReplyUpdate(APIView):
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = ReplySerializer

    def patch(self, request, comment_id, reply_id):
        comment = get_object_or_404(Comment.active, id=comment_id)
        reply = get_object_or_404(Reply, comment=comment, pk=reply_id)

        self.check_object_permissions(request, reply)

        serializer = self.serializer_class(
            instance=reply,
            data=request.data,
            partial=True,
            context={"request": request},
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReplyDelete(APIView):
    permission_classes = [
        IsOwnerOrReadOnly,
    ]
    serializer_class = ReplySerializer

    def delete(self, request, comment_id, reply_id):
        comment = get_object_or_404(Comment.active, id=comment_id)
        reply = get_object_or_404(Reply, comment=comment, pk=reply_id)

        self.check_object_permissions(request, reply)

        reply.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ArticleLike(APIView):
    permission_classes = [
        IsAuthenticated,
    ]

    def post(self, request, article_id):
        article = get_object_or_404(Article, id=article_id)
        if article.likes.filter(id=request.user.id).exists():
            article.likes.remove(request.user)
        else:
            article.likes.add(request.user)
        data = article.likes.count()
        return Response(data, status=status.HTTP_201_CREATED)
