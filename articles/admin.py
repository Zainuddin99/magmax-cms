from django.contrib import admin
from .models import Article, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'status', 'published_date', 'view_count', 'created_at']
    list_filter = ['status', 'published_date', 'created_at', 'categories']
    search_fields = ['title', 'content', 'meta_keywords']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['created_at', 'updated_at', 'view_count', 'reading_time']
    filter_horizontal = ['categories']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'excerpt', 'content', 'featured_image')
        }),
        ('Classification', {
            'fields': ('author', 'categories', 'status')
        }),
        ('Publishing', {
            'fields': ('published_date',)
        }),
        ('SEO Settings', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords'),
            'classes': ('collapse',)
        }),
        ('Open Graph / Social Media', {
            'fields': ('og_title', 'og_description', 'og_image'),
            'classes': ('collapse',)
        }),
        ('Analytics', {
            'fields': ('view_count', 'reading_time'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        """Auto-assign the current user as author if creating new article"""
        if not change:
            obj.author = request.user
        super().save_model(request, obj, form, change)
