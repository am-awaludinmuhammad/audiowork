from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', include('main.urls')),  # Include the main app's URLs
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)