from django.contrib import admin
from servis.models import Alet, Teknisyen, AletHareketi, Raf

@admin.register(Alet)
class AletAdmin(admin.ModelAdmin):
    list_display = ('isim', 'marka', 'model', 'raf', 'durum', 'teknisyen')
    list_filter = ('durum', 'raf', 'teknisyen')
    search_fields = ('isim', 'marka', 'model')

@admin.register(Teknisyen)
class TeknisyenAdmin(admin.ModelAdmin):
    list_display = ('isim', 'telefon')
    search_fields = ('isim',)

@admin.register(AletHareketi)
class AletHareketiAdmin(admin.ModelAdmin):
    list_display = ('alet', 'teknisyen', 'alinma_zamani', 'teslim_zamani')
    list_filter = ('alet', 'teknisyen')

@admin.register(Raf)
class RafAdmin(admin.ModelAdmin):
    list_display = ('isim',)
    search_fields = ('isim',)
