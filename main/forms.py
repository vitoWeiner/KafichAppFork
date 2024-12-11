from django import forms
from django.contrib.auth.models import User, Group


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