from rest_framework import serializers
from .models import Article, Category
from core.models import Comment, Reply

from django.contrib.auth import get_user_model

User = get_user_model()


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')


class ArticleSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        remove_fields = kwargs.pop('remove_fields', None)
        fields = kwargs.pop('fields', None)
        super(ArticleSerializer, self).__init__(*args, **kwargs)

        if remove_fields:
            # for multiple fields in a list
            for field_name in remove_fields:
                self.fields.pop(field_name)


    author = AuthorSerializer()
    category = serializers.SerializerMethodField()
    article_likes_count = serializers.ReadOnlyField(source="likes_count")

    class Meta:
        model = Article
        fields = ['id', 'slug', 'author', 'category', 'title',
                  'description', 'cover', 'created', 'updated',
                  'article_likes_count']

    def get_category(self, obj):
        return {
            'name': obj.category.name,
            'slug': obj.category.slug,
        }


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


from generic_relations.relations import GenericRelatedField

class CommentSerializer(serializers.ModelSerializer):
    replies = serializers.HyperlinkedIdentityField(
        view_name="blog:comment-replies")
    user = serializers.SerializerMethodField("get_user")
    parent = GenericRelatedField({
        Article: ArticleSerializer(remove_fields=['slug', 'author', 'category', 'title',
                  'description', 'cover', 'created', 'updated',
                  'article_likes_count'])
    })

    class Meta:
        model = Comment
        fields = ('id', 'user', 'parent', 'body', 'created', 'replies')

    def get_user(self, obj):
        if obj.user:
            return obj.user.username,
        else:
            return None
    


class ReplySerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    comment = serializers.SerializerMethodField()

    class Meta:
        model = Reply
        fields = '__all__'

    def get_user(self, obj):
        if obj.user:
            return obj.user.username,
        else:
            return None

    def get_comment(self, obj):
        return {
            'id': obj.comment.id, 
            'body': obj.comment.body
        }
    
    def validate(self, attrs):
        return super().validate(attrs)
    
    def create(self, validated_data):
        return super().create(validated_data)
