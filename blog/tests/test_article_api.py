from django.test import TestCase
from rest_framework.test import APIClient
from model_bakery import baker
from django.urls import reverse
from ..models import Article, Category
from ..serializers import ArticleSerializer, CategorySerializer


class PublicAPIArticleTest(TestCase):
    """
    Will test some endpoints that an unauthorised user can see
    """

    def setUp(self):
        # making client
        self.client = APIClient()

        self.article = baker.make(
            Article, _fill_optional=True, _create_files=True, tags='', description='')

    def test_list_api_view(self):
        """Tests the list of articles"""

        second_article = baker.make(Article, _fill_optional=True, _create_files=True,
                                    tags='', description='')  # TODO: should i use .save()
        articles = Article.objects.all()
        res = self.client.get(reverse('blog:list'))

        sz_data = ArticleSerializer(articles, many=True, remove_fields=[
                                     'created', 'description'])

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['results'], sz_data.data)

    def test_article_detail_view(self):
        """Tests single article data"""

        res = self.client.get(
            reverse('blog:detail', args=(self.article.slug,)))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['title'], self.article.title)
        self.assertEqual(res.data['slug'], self.article.slug)


    # def test_article_by_category(self):
    #     """Tests articles by fetching them from their category"""

    #     res = self.client.get(reverse('blog:article_by_category', kwargs={
    #                           'category': self.article.category.slug}))
    #     articles = Article.active.filter(category=self.article.category)

    #     sz = ArticleSerializer(articles, many=True)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(res.data['results'], sz.data)

    # def test_category_list_view(self):
    #     """Tests list of active categories"""

    #     Category.objects.create(name='react', slug='react')
    #     res = self.client.get(reverse('blog:category_list'))
    #     categories = Category.active.all()

    #     sz = CategorySerializer(categories, many=True)
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(res.data['results'], sz.data)
