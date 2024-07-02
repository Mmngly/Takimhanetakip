from django.urls import path
from . import views
from ozel_admin import views as ozel_admin_views

urlpatterns = [
    path('', views.takimhane_anasayfa, name='takimhane_anasayfa'),  # Ana sayfa için views.takimhane_anasayfa kullanılıyor
    path('aletler/', ozel_admin_views.alet_listesi, name='alet_listesi'),  # Özel admin alet listesi için farklı bir URL
    path('alet/<int:alet_id>/', views.alet_detay, name='alet_detay'),
    path('rapor-olustur/', views.olustur_gunluk_rapor, name='olustur_gunluk_rapor'),
    path('alet/<int:alet_id>/ver/', views.alet_ver, name='alet_ver'),
];
