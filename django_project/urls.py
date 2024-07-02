from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ozel_admin/', include('ozel_admin.urls')),  # Özel admin paneli için
    path('', include('servis.urls')),  # Ana sayfa için
]
