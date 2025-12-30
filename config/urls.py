"""
URL configuration for config project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

# Non-i18n URLs
urlpatterns = [
    # API endpoints
    path('api/v1/', include('articles.urls')),
    
    # JWT Authentication
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    # REST Framework browsable API
    path('api-auth/', include('rest_framework.urls')),
]

# i18n URLs (for Django CMS)
urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('', include('cms.urls')),
)

# Media files (only in development)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
