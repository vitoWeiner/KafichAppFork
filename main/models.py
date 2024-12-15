from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator
import uuid

# Create your models here.
class Pice(models.Model):
    pice_sifra = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)    #models.CharField(max_length=10, unique=True, blank=True)
    pice_naziv = models.CharField(max_length=30)
    pice_opis = models.CharField(max_length=100)
    pice_kolicina_u_ml = models.FloatField()
    pice_sadrzi_alkohol = models.BooleanField(default=False)
    pice_vegansko = models.BooleanField(default=False)
    pice_poj_cijena = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.pice_sifra



class Konobar(models.Model):
    konobar_korisnicko_ime = models.CharField(max_length=30, unique=True)    
    konobar_zaporka = models.CharField(max_length=128)  
    konobar_ime = models.CharField(max_length=50)
    konobar_prezime = models.CharField(max_length=50)
    konobar_datum_zaposlenja = models.DateField(auto_now_add=True)
    konobar_zarada = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, validators=[MinValueValidator(0.00)])
    konobar_email = models.EmailField(unique=True)
    konobar_telefon = models.CharField(max_length=15, null=True, blank=True)
    

    def __str__(self):
        return self.konobar_korisnicko_ime



class Narudzba(models.Model):
    narudzba_sifra =  models.UUIDField(default=uuid.uuid4, editable=False, unique=True)                 # models.CharField(max_length=10)
    narudzba_kolicina_stavki = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]  
    )
    narudzba_konobar = models.ForeignKey(
        Konobar, 
        on_delete=models.CASCADE,  
        related_name='narudzbe'    
    )
    narudzba_datum_kreiranja = models.DateTimeField(default=timezone.now)
    narudzba_placena = models.BooleanField(default=False)  


    def __str__(self):
        return self.narudzba_sifra


class StavkaNarudzbe(models.Model):
    stavka_narudzba = models.ForeignKey(
        Narudzba, 
        on_delete=models.CASCADE, 
        related_name='stavke'
    )
    stavka_pice = models.ForeignKey(
        Pice, 
        on_delete=models.CASCADE, 
        related_name='stavke_u_narudzbama'
    )
    stavka_kolicina_pica = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )

    stavka_ukupna_cijena = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(0.00)],
        default=0.00
    )     

    def save(self, *args, **kwargs):
        
        self.stavka_ukupna_cijena = self.stavka_kolicina_pica * self.stavka_pice.pice_poj_cijena
        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.stavka_narudzba.narudzba_sifra} - {self.stavka_pice.pice_naziv} (x{self.stavka_kolicina_pica})"
