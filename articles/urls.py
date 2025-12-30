from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ArticleViewSet, CategoryViewSet

# Create router and register viewsets
router = DefaultRouter()
router.register(r'articles', ArticleViewSet, basename='article')
router.register(r'categories', CategoryViewSet, basename='category')

app_name = 'articles'

urlpatterns = [
    path('', include(router.urls)),
]



