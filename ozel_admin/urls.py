from django.urls import path
from . import views

urlpatterns = [
     path('', views.ozel_admin_anasayfa, name='ozel_admin_anasayfa'),
     path('aletler/', views.alet_listesi, name='alet_listesi'),
     path('aletler/ekle/', views.alet_ekle, name='alet_ekle'),
     path('teknisyenler/ekle/', views.teknisyen_ekle, name='teknisyen_ekle'),
     path('raporlar/', views.raporlar, name='raporlar'),
     path('alet-autocomplete/', views.AletAutocomplete.as_view(), name='alet-autocomplete'),
     path('teknisyen-autocomplete/', views.TeknisyenAutocomplete.as_view(), name='teknisyen-autocomplete'),
     path('raf-autocomplete/', views.RafAutocomplete.as_view(), name='raf-autocomplete'),
     path('raflar/ekle/', views.raf_ekle, name='raf_ekle'),
 ];
