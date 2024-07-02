from django.db import models

class Alet(models.Model):
    DURUM_SECENEKLERI = [
        ('bakimda', 'Bakımda'),
        ('teknisyende', 'Teknisyende'),
        ('rafta', 'Rafta'),
    ]
    isim = models.CharField(max_length=100)
    marka = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    raf = models.ForeignKey('Raf', on_delete=models.SET_NULL, null=True, blank=True)
    durum = models.CharField(max_length=20, choices=DURUM_SECENEKLERI, default='rafta')
    teknisyen = models.ForeignKey('Teknisyen', on_delete=models.SET_NULL, null=True, blank=True)

class Teknisyen(models.Model):
    isim = models.CharField(max_length=100)
    telefon = models.CharField(max_length=15, default="")

class AletHareketi(models.Model):
    alet = models.ForeignKey(Alet, on_delete=models.CASCADE)
    teknisyen = models.ForeignKey(Teknisyen, on_delete=models.CASCADE)
    alinma_zamani = models.DateTimeField(auto_now_add=True)
    teslim_zamani = models.DateTimeField(null=True, blank=True)

class Raf(models.Model):
    isim = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.isim
