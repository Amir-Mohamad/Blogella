from django.shortcuts import render
from rest_framework import viewsets
from .models import Book
from .serializers import BookSerializer


class BookViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Book.active.all()
    serializer_class = BookSerializer
