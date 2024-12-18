from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator
import uuid
from django.contrib.auth.models import User

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
        return self.pice_naziv



class Konobar(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='konobar', null=True, blank=True)    
    konobar_ime = models.CharField(max_length=50)
    konobar_prezime = models.CharField(max_length=50)
    konobar_datum_zaposlenja = models.DateField(auto_now_add=True)
    konobar_zarada = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, validators=[MinValueValidator(0.00)])
    konobar_telefon = models.CharField(max_length=15, null=True, blank=True)
    

    def __str__(self):
        return self.konobar_ime




class Narudzba(models.Model):
    narudzba_sifra =  models.UUIDField(default=uuid.uuid4, editable=False, unique=True)                 # models.CharField(max_length=10)
    narudzba_kolicina_stavki = models.PositiveIntegerField(
        validators=[MinValueValidator(0)],
        blank = True  
    )
    narudzba_konobar = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,  
        related_name='narudzbe'    
    )
    narudzba_datum_kreiranja = models.DateTimeField(default=timezone.now)
    narudzba_placena = models.BooleanField(default=False)  
    narudzba_ukupna_cijena = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def update_ukupna_cijena(self):
        total_price = sum(stavka.stavka_ukupna_cijena for stavka in self.stavke.all())
        self.narudzba_ukupna_cijena = total_price
        self.save()

    def __str__(self):
        return self.narudzba_sifra


class StavkaNarudzbe(models.Model):


    stavka_sifra = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)



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
