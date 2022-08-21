from book.models import Category
from django.test import TestCase
from django.urls import reverse
from model_bakery import baker
from rest_framework.test import APIClient
from ..models import Book
from ..serializers import BookSerializer


class PublicAPIBookTest(TestCase):
    """
    Will test some endpoints that an unauthorised user can see
    """

    def setUp(self):
        # making client
        self.client = APIClient()

        self.book = baker.make(
            Book, _create_files=True, tags="", content="", is_active=True, cover=""
        )
        # self.book = mixer.blend('book.book', content='', tags='')

    def test_list_api_view(self):
        """Tests the list of books"""

        baker.make(
            Book, _create_files=True, tags="", content="", is_active=True, cover=""
        )

        books = Book.objects.all()
        res = self.client.get(reverse("book:book-list"))
        sz_data = BookSerializer(books, many=True)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["results"], sz_data.data)

    def test_book_detail_view(self):
        """Tests single book data"""

        res = self.client.get(reverse("book:book-detail", args=(self.book.id,)))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["title"], self.book.title)
        self.assertEqual(res.data["slug"], self.book.slug)
