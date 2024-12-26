from django import forms
from django.contrib.auth.models import User, Group

from .models import *
from django.contrib.auth.forms import UserCreationForm

from django.core.exceptions import ValidationError 
from django.contrib.auth.forms import UserChangeForm

# forma za kreiranje novog konobara (iz sucelja administratora, administrator kreira novog korisnika)

class KonobarCreationForm(forms.ModelForm):

    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)    # required dal treba?
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)

    konobar_ime = forms.CharField(label="First Name", required=True)
    konobar_prezime = forms.CharField(label="Last Name", required=True)
    konobar_telefon = forms.CharField(label="Phone", required=False)

    class Meta:
        model = User
        fields = ['username', 'email']


    def clean_password2(self):

        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):

        user = super(KonobarCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])  
            
        if commit:
            user.save()

        group = Group.objects.get(name='Korisnik')
        group.user_set.add(user)


        konobar = Konobar.objects.create(
            user=user,  
            konobar_ime=self.cleaned_data.get("konobar_ime"),
            konobar_prezime=self.cleaned_data.get("konobar_prezime"),
            konobar_telefon=self.cleaned_data.get("konobar_telefon"),
        )

        return user  


# forma za kreiranje novog administratora iz sucelja admina:

class AdminCreationForm(forms.ModelForm):

    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ['username', 'email']  

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super(AdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])  
        
        if commit:
            user.save()

       
        group = Group.objects.get(name='Administrator')  
        group.user_set.add(user)  

        return user


# registracija konobara samostalno, ne od strane admina

class KonobarRegisterForm(UserCreationForm):

    konobar_ime = forms.CharField(label="Ime", required=True)
    konobar_prezime = forms.CharField(label="Prezime", required=True)
    konobar_telefon = forms.CharField(label="Telefon", required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)  

        if commit:
            user.save()  

        group = Group.objects.get(name='Korisnik')  
        group.user_set.add(user)  

       
        Konobar.objects.create(
            user=user,
            konobar_ime=self.cleaned_data['konobar_ime'],
            konobar_prezime=self.cleaned_data['konobar_prezime'],
            konobar_telefon=self.cleaned_data.get('konobar_telefon')
        )
        return user


# registracija novog pica od strane admina:

class PiceForm(forms.ModelForm):
    class Meta:
        model = Pice
        fields = ['pice_naziv', 'pice_opis', 'pice_kolicina_u_ml', 'pice_sadrzi_alkohol', 'pice_vegansko', 'pice_poj_cijena']

    pice_naziv = forms.CharField(required=True)
    pice_kolicina_u_ml = forms.IntegerField(min_value=1, required=True, label="Količina (ml)")
    pice_poj_cijena = forms.DecimalField(min_value=0.01, max_digits=10, decimal_places=2, required=True, label="Cijena (€)")




# kreiranje nove narudzbe (od strane konobara)

class NarudzbaForm(forms.ModelForm):
    class Meta:
        model = Narudzba
        fields = ['narudzba_kolicina_stavki', 'narudzba_placena']
        widgets = {
            'narudzba_kolicina_stavki': forms.HiddenInput()  
        }


# dodavanje stavke narudzbe od strane konobara:

class StavkaNarudzbeForm(forms.ModelForm):
    class Meta:
        model = StavkaNarudzbe
        fields = ['stavka_pice', 'stavka_kolicina_pica']


# forma za azuriranje konobara od strane samog konobara:

class KonobarForm(forms.ModelForm):
    class Meta:
        model = Konobar
        fields = ['konobar_ime', 'konobar_prezime', 'konobar_telefon']

    def clean_konobar_telefon(self):
        telefon = self.cleaned_data.get('konobar_telefon')
        if telefon and not telefon.isdigit():
            raise forms.ValidationError("Telefon mora sadržavati samo brojeve.")
        return telefon


# UserForm - za azuriranje konobara, tablice User

class UserForm(UserChangeForm):


    password = None

    class Meta:
        model = User
        fields = ['username', 'email']
   
    


class StavkaNarudzbeForm(forms.ModelForm):
    class Meta:
        model = StavkaNarudzbe
        fields = ['stavka_kolicina_pica', 'stavka_pice']

    stavka_pice = forms.ModelChoiceField(queryset=Pice.objects.all(), empty_label="Izaberi piće")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['stavka_pice'].queryset = Pice.objects.all()  

    def clean_stavka_kolicina_pica(self):
        kolicina = self.cleaned_data.get('stavka_kolicina_pica')
        if kolicina <= 0:
            raise forms.ValidationError("Količina mora biti veća od nule.")
        return kolicina

"""
class UserCreationWithGroupForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)
    
    group = forms.ModelChoiceField(queryset=Group.objects.all(), required=True, label="Role")

    konobar_ime = forms.CharField(label="First Name", required=True)
    konobar_prezime = forms.CharField(label="Last Name", required=True)
    konobar_telefon = forms.CharField(label="Phone", required=False)


    class Meta:
        model = User
        fields = ['username', 'email']  

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        
        # Dodavanje korisnika u odabranu grupu
        group = self.cleaned_data.get("group")
        group.user_set.add(user)


        if group.name == 'Konobar':
            Konobar.objects.create(
                user = user,
                konobar_ime = self.cleaned_data.get("konobar_ime"),
                konobar_prezime = self.cleaned_data.get("konobar_prezime"),
                konobar_telefon = self.cleaned_data.get("konobar_telefon"),
            )

        return user

"""

