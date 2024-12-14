from django import forms
from django.contrib.auth.models import User, Group

from .models import *


class UserCreationWithGroupForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)
    
    group = forms.ModelChoiceField(queryset=Group.objects.all(), required=True, label="Role") # dropdown za izbor grupe

    class Meta:
        model = User
        fields = ['username', 'email']  # Polja za unos u formi

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])  # Postavljanje lozinke
        if commit:
            user.save()
        
        # Dodavanje korisnika u odabranu grupu
        group = self.cleaned_data.get("group")
        group.user_set.add(user)
        return user


# forma za unos novog pica:

class PiceForm(forms.ModelForm):
    class Meta:
        model = Pice
        fields = ['pice_naziv', 'pice_opis', 'pice_kolicina_u_ml', 'pice_sadrzi_alkohol', 'pice_vegansko', 'pice_poj_cijena']

    pice_naziv = forms.CharField(required=True)
    pice_kolicina_u_ml = forms.IntegerField(required=True)
