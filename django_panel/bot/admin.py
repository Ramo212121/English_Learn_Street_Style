from django.contrib import admin
from .models import Cumle, Kullanici, Cevap


@admin.register(Cumle)
class CumleAdmin(admin.ModelAdmin):
    list_display = ('id', 'seviye', 'gun', 'ingilizce', 'turkce', 'baglam')
    list_filter = ('seviye', 'gun', 'baglam')
    search_fields = ('ingilizce', 'turkce')
    ordering = ('gun', 'id')


@admin.register(Kullanici)
class KullaniciAdmin(admin.ModelAdmin):
    list_display = ('id', 'isim', 'seviye', 'dogru_sayisi', 'yanlis_sayisi', 'kufur_sayisi', 'streak', 'son_aktivite')
    list_filter = ('seviye',)
    search_fields = ('isim',)
    ordering = ('-son_aktivite',)


@admin.register(Cevap)
class CevapAdmin(admin.ModelAdmin):
    list_display = ('id', 'kullanici_id', 'cumle_id', 'dogru_mu', 'aralik', 'tekrar', 'tarih', 'sonraki_sorulma')
    list_filter = ('dogru_mu',)
    ordering = ('-tarih',)