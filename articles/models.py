from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils import timezone
from filer.fields.image import FilerImageField


class Category(models.Model):
    """Category model for organizing articles"""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Article(models.Model):
    """Article model with SEO fields"""
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]
    
    # Basic Fields
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    excerpt = models.TextField(max_length=500, blank=True, help_text="Brief description of the article")
    content = models.TextField()
    
    # Image
    featured_image = FilerImageField(
        null=True,
        blank=True,
        related_name="article_featured_image",
        on_delete=models.SET_NULL
    )
    
    # Relationships
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles')
    categories = models.ManyToManyField(Category, related_name='articles', blank=True)
    
    # Status & Dates
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    published_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # SEO Fields
    meta_title = models.CharField(
        max_length=60, 
        blank=True,
        help_text="SEO meta title (max 60 chars, leave blank to use article title)"
    )
    meta_description = models.CharField(
        max_length=160,
        blank=True,
        help_text="SEO meta description (max 160 chars)"
    )
    meta_keywords = models.CharField(
        max_length=255,
        blank=True,
        help_text="Comma-separated keywords for SEO"
    )
    
    # Open Graph / Social Media
    og_title = models.CharField(
        max_length=95,
        blank=True,
        help_text="Open Graph title (leave blank to use meta_title or title)"
    )
    og_description = models.CharField(
        max_length=200,
        blank=True,
        help_text="Open Graph description"
    )
    og_image = FilerImageField(
        null=True,
        blank=True,
        related_name="article_og_image",
        on_delete=models.SET_NULL,
        help_text="Image for social media sharing (leave blank to use featured_image)"
    )
    
    # Analytics
    view_count = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['-published_date', '-created_at']
        indexes = [
            models.Index(fields=['-published_date']),
            models.Index(fields=['slug']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        # Auto-generate slug from title if not provided
        if not self.slug:
            self.slug = slugify(self.title)
        
        # Auto-manage published_date based on status
        if self.status == 'published' and self.published_date is None:
            # When changing from draft -> published without a date, set now
            self.published_date = timezone.now()
        elif self.status != 'published':
            # For draft/archived, we can clear published_date so filters behave predictably
            self.published_date = None
        
        # Auto-fill SEO fields if not provided
        if not self.meta_title:
            self.meta_title = self.title[:60]
        
        if not self.meta_description and self.excerpt:
            self.meta_description = self.excerpt[:160]
        
        if not self.og_title:
            self.og_title = self.meta_title[:95]
        
        if not self.og_description:
            self.og_description = self.meta_description[:200]
        
        super().save(*args, **kwargs)
    
    @property
    def is_published(self):
        """Check if article is published"""
        return self.status == 'published' and self.published_date is not None
    
    @property
    def reading_time(self):
        """Calculate estimated reading time in minutes"""
        words_per_minute = 200
        word_count = len(self.content.split())
        return max(1, round(word_count / words_per_minute))
    
    def get_seo_image(self):
        """Get the appropriate image for SEO/OG tags"""
        return self.og_image or self.featured_image
