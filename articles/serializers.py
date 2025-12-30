from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Article, Category


class AuthorSerializer(serializers.ModelSerializer):
    """Serializer for article author"""
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for categories"""
    article_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'article_count', 'created_at', 'updated_at']
        read_only_fields = ['slug', 'created_at', 'updated_at']
    
    def get_article_count(self, obj):
        """Get count of published articles in this category"""
        return obj.articles.filter(status='published').count()


class ArticleListSerializer(serializers.ModelSerializer):
    """Serializer for article list view (minimal data)"""
    author = AuthorSerializer(read_only=True)
    categories = CategorySerializer(many=True, read_only=True)
    featured_image_url = serializers.SerializerMethodField()
    reading_time = serializers.ReadOnlyField()
    
    class Meta:
        model = Article
        fields = [
            'id', 'title', 'slug', 'excerpt', 'featured_image_url',
            'author', 'categories', 'status', 'published_date',
            'reading_time', 'view_count', 'created_at'
        ]
    
    def get_featured_image_url(self, obj):
        """Get featured image URL"""
        if obj.featured_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.featured_image.url)
            return obj.featured_image.url
        return None


class ArticleDetailSerializer(serializers.ModelSerializer):
    """Serializer for article detail view (complete data including SEO)"""
    author = AuthorSerializer(read_only=True)
    categories = CategorySerializer(many=True, read_only=True)
    featured_image_url = serializers.SerializerMethodField()
    og_image_url = serializers.SerializerMethodField()
    reading_time = serializers.ReadOnlyField()
    is_published = serializers.ReadOnlyField()
    
    # SEO fields
    seo = serializers.SerializerMethodField()
    
    class Meta:
        model = Article
        fields = [
            'id', 'title', 'slug', 'excerpt', 'content',
            'featured_image_url', 'og_image_url', 'author', 'categories',
            'status', 'published_date', 'created_at', 'updated_at',
            'reading_time', 'view_count', 'is_published',
            'seo'
        ]
    
    def get_featured_image_url(self, obj):
        """Get featured image URL"""
        if obj.featured_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.featured_image.url)
            return obj.featured_image.url
        return None
    
    def get_og_image_url(self, obj):
        """Get Open Graph image URL"""
        image = obj.get_seo_image()
        if image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(image.url)
            return image.url
        return None
    
    def get_seo(self, obj):
        """Get all SEO-related data"""
        return {
            'meta_title': obj.meta_title or obj.title,
            'meta_description': obj.meta_description or obj.excerpt,
            'meta_keywords': obj.meta_keywords,
            'og_title': obj.og_title or obj.meta_title or obj.title,
            'og_description': obj.og_description or obj.meta_description or obj.excerpt,
            'og_image': self.get_og_image_url(obj),
        }


class ArticleCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating and updating articles"""
    
    class Meta:
        model = Article
        fields = [
            'title', 'slug', 'excerpt', 'content',
            'featured_image', 'categories', 'status', 'published_date',
            'meta_title', 'meta_description', 'meta_keywords',
            'og_title', 'og_description', 'og_image'
        ]
        extra_kwargs = {
            'slug': {'required': False},
        }
    
    def create(self, validated_data):
        """Create article with current user as author"""
        categories = validated_data.pop('categories', [])
        validated_data['author'] = self.context['request'].user
        article = Article.objects.create(**validated_data)
        article.categories.set(categories)
        return article



