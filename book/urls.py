from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.SimpleRouter()
router.register(r'', views.BookViewSet)

app_name = 'book'
urlpatterns = router.urls