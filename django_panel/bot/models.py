from django.db import models


class Cumle(models.Model):
    """İngilizce cümleler."""
    gun = models.IntegerField()
    seviye = models.CharField(max_length=5)
    ingilizce = models.TextField()
    turkce = models.TextField()
    baglam = models.CharField(max_length=50, blank=True)
    ipucu = models.TextField(blank=True)
    varyasyonlar = models.TextField(blank=True, help_text="JSON array olarak")

    class Meta:
        db_table = 'cumleler'
        managed = False
        verbose_name = "Cümle"
        verbose_name_plural = "Cümleler"

    def __str__(self):
        return f"[{self.seviye}] {self.ingilizce}"


class Kullanici(models.Model):
    """Kullanıcılar."""
    isim = models.CharField(max_length=100)
    seviye = models.CharField(max_length=5, default='A1')
    kufur_sayisi = models.IntegerField(default=0)
    dogru_sayisi = models.IntegerField(default=0)
    yanlis_sayisi = models.IntegerField(default=0)
    streak = models.IntegerField(default=0)
    son_aktivite = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'kullanicilar'
        managed = False
        verbose_name = "Kullanıcı"
        verbose_name_plural = "Kullanıcılar"

    def __str__(self):
        return f"{self.isim} ({self.seviye})"


class Cevap(models.Model):
    """Kullanıcı cevapları."""
    kullanici_id = models.IntegerField()
    cumle_id = models.IntegerField()
    dogru_mu = models.BooleanField()
    tarih = models.DateTimeField(auto_now=True)
    sonraki_sorulma = models.DateTimeField(null=True, blank=True)
    aralik = models.IntegerField(default=0)
    kolaylik = models.FloatField(default=2.5)
    tekrar = models.IntegerField(default=0)

    class Meta:
        db_table = 'cevaplar'
        managed = False
        verbose_name = "Cevap"
        verbose_name_plural = "Cevaplar"

    def __str__(self):
        durum = "✅" if self.dogru_mu else "❌"
        return f"{durum} Kullanıcı {self.kullanici_id} - Cümle {self.cumle_id}"