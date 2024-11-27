from django.db import models
from django.utils import timezone
# Create your models here.
class Pice(models.Model):
    pice_sifra = models.CharField(max_length=10)
    pice_naziv = models.CharField(max_length=30)
    pice_opis = models.CharField(max_length=100)
    pice_kolicina_u_ml = models.FloatField()
    pice_sadrzi_alkohol = models.BooleanField(default=False)
    pice_vegansko = models.BooleanField(default=False)
    pice_poj_cijena = models.FloatField()


    def __str__(self):
        return self.pice_sifra