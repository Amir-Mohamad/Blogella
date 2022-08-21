from rest_framework import serializers
from .models import Book


class BookSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        remove_fields = kwargs.pop("remove_fields", None)
        fields = kwargs.pop("fields", None)
        super(BookSerializer, self).__init__(*args, **kwargs)

        if remove_fields:
            # for multiple fields in a list
            for field_name in remove_fields:
                self.fields.pop(field_name)

    author = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = "__all__"

    def get_category(self, obj):
        return {
            "id": obj.category.id if obj.category else None,
            "name": obj.category.name if obj.category else None,
        }

    def get_author(self, obj):
        if obj.author:
            return (obj.author.username,)
        else:
            return None
