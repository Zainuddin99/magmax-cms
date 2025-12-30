from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from django.db import models
from .models import Article, Category
from .serializers import (
    ArticleListSerializer,
    ArticleDetailSerializer,
    ArticleCreateUpdateSerializer,
    CategorySerializer
)


class ArticleViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Article model
    
    Provides CRUD operations for articles with filtering, search, and ordering.
    Public users can read published articles, authenticated users can manage articles.
    """
    queryset = Article.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'author', 'categories', 'published_date']
    search_fields = ['title', 'excerpt', 'content', 'meta_keywords']
    ordering_fields = ['published_date', 'created_at', 'view_count', 'title']
    ordering = ['-published_date']
    lookup_field = 'slug'
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'list':
            return ArticleListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return ArticleCreateUpdateSerializer
        return ArticleDetailSerializer
    
    def get_queryset(self):
        """
        Filter queryset based on user authentication.
        Public users only see published articles.
        Authenticated users see all their articles.
        """
        queryset = Article.objects.select_related('author').prefetch_related('categories')
        
        # If user is not authenticated, only show published articles
        if not self.request.user.is_authenticated:
            queryset = queryset.filter(status='published')
        else:
            # Authenticated users can see their own articles and published ones
            if not self.request.user.is_staff:
                queryset = queryset.filter(
                    models.Q(author=self.request.user) | 
                    models.Q(status='published')
                )
        
        return queryset
    
    def retrieve(self, request, *args, **kwargs):
        """Increment view count when article is retrieved"""
        instance = self.get_object()
        
        # Increment view count for published articles
        if instance.status == 'published':
            instance.view_count += 1
            instance.save(update_fields=['view_count'])
        
        serializer = self.get_serializer(instance, context={'request': request})
        return Response(serializer.data)
    
    def list(self, request, *args, **kwargs):
        """List articles with proper request context for image URLs"""
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def published(self, request):
        """Get only published articles"""
        queryset = Article.objects.select_related('author').prefetch_related('categories').filter(
            status='published'
        )
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = ArticleListSerializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        
        serializer = ArticleListSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Get featured articles (most viewed published articles)"""
        queryset = Article.objects.select_related('author').prefetch_related('categories').filter(
            status='published'
        ).order_by('-view_count')[:5]
        
        serializer = ArticleListSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_articles(self, request):
        """Get current user's articles"""
        queryset = self.get_queryset().filter(author=request.user)
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = ArticleListSerializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        
        serializer = ArticleListSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)


class CategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Category model
    
    Provides CRUD operations for categories.
    Public users can read, authenticated users can manage categories.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']
    
    @action(detail=True, methods=['get'])
    def articles(self, request, slug=None):
        """Get all published articles in this category"""
        category = self.get_object()
        articles = category.articles.filter(status='published')
        
        page = self.paginate_queryset(articles)
        if page is not None:
            serializer = ArticleListSerializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        
        serializer = ArticleListSerializer(articles, many=True, context={'request': request})
        return Response(serializer.data)
