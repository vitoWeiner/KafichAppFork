from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group  # Dodano
from .forms import *
from django.views.generic import ListView, DetailView
from .models import *
from django.db.models import Q
from django_filters import *

from django.forms import inlineformset_factory
from django.contrib.auth.mixins import LoginRequiredMixin


 ## ## # from django.contrib.auth.models import User

## Create your views here.
@login_required
def homepage(request):

    if request.user.groups.filter(name='Korisnik').exists():
        print("User is part of the Korisnik group.")
        return render(request, 'main/user/user_homepage.html')
    else: 
        print('user is admin')
        return render(request, 'main/admin/admin_homepage.html')


    #return render(request, 'main/homepage.html')    # DJANGO automatski trazi html datoteku pod templates folder, zbog postavke u settingsima APP_DIRS = True, svaka app ce imati svoj templates folder
    #return HttpResponse('Welcome to our homepage! <strong>#samoKAFICH</strong>')    



 

def register(request):
    if request.method == 'POST':
        form = KonobarRegisterForm(request.POST)  
        if form.is_valid():  
            user = form.save()  

            #group = Group.objects.get(name='Korisnik')  
            #group.user_set.add(user)  


           # Konobar.objects.create(user=user)


            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password) 
            login(request, user) 
            return redirect('main:homepage') 
    else:
        form = KonobarRegisterForm()  

    context = {'form': form}
    return render(request, 'registration/register.html', context)

def register_superuser(request):

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = True
            user.is_superuser = True
            user.save()


            group = Group.objects.get(name='Administrator')
            group.user_set.add(user) 


            return redirect('login')  # Redirektuje na login stranicu
    else:
        form = UserCreationForm()

    return render(request, 'registration/register_super_user.html', {'form': form})




@login_required
def manage_users(request):
    if request.user.groups.filter(name='Korisnik').exists():
        return redirect('main:homepage')  

    users = User.objects.all()  
    return render(request, 'main/admin/upravljanje_korisnicima/manage_users.html', {'users': users})




@login_required
def edit_user(request, user_id):
    if request.user.groups.filter(name='Korisnik').exists():
        return redirect('main:homepage')

    user = User.objects.get(id=user_id)
    if request.method == 'POST':
        user.username = request.POST.get('username', user.username)
        user.email = request.POST.get('email', user.email)
        user.save()
        return redirect('main:manage_users')

    return render(request, 'main/admin/upravljanje_korisnicima/uredivanje_korisnika/edit_user.html', {'user': user})

@login_required
def delete_user(request, user_id):
    if request.user.groups.filter(name='Korisnik').exists():
        return redirect('main:homepage')

    user = User.objects.get(id=user_id)
    if request.method == 'POST':
        user.delete()
        return redirect('main:manage_users')

    return render(request, 'main/admin/upravljanje_korisnicima/brisanje_korisnika/delete_user.html', {'user': user})




@login_required
def add_user(request):
    
    #if not request.user.groups.filter(name='Korisnik').exists():
    return render(request, 'main/admin/upravljanje_korisnicima/dodavanje_novog_korisnika/add_user.html')
    #else:
     #   return redirect('main:homepage')



def add_admin(request):
    if request.method == 'POST':
        form = AdminCreationForm(request.POST)
        if form.is_valid():
            form.save()  
            return redirect('main:manage_users')
    else:
        form = AdminCreationForm()

    return render(request, 'main/admin/upravljanje_korisnicima/dodavanje_novog_korisnika/dodavanje_novog_administratora/add_admin.html', {'form': form})



def add_konobar(request):
    if request.method == 'POST':
        form = KonobarCreationForm(request.POST)
        if form.is_valid():
            form.save() 
            return redirect('main:manage_users')  
    else:
        form = KonobarCreationForm()

    return render(request, 'main/admin/upravljanje_korisnicima/dodavanje_novog_korisnika/dodavanje_novog_Konobara/add_konobar.html', {'form': form})


@login_required
def show_other_users(request):
   
    if request.user.groups.filter(name='Korisnik').exists() and not request.user.is_superuser:
        
        users = User.objects.exclude(id=request.user.id)
        return render(request, 'main/user/lista_ostalih_korisnika/show_other_users.html', {'users': users})
    else:
       
        return redirect('main:manage_users')



"""
@login_required
def drinks_list_view(request):
   
    # dodati uvjet da nije korisnik nego admin samo

    return render(request, 'main/admin/lista_pica/ListView.html')

"""


class PiceListView(ListView):
    model = Pice
    template_name = 'main/admin/lista_pica/list_view.html'
    context_object_name = 'pica'
    paginate_by = 10


    def get_queryset(self):
        queryset = super().get_queryset()

        search = self.request.GET.get('search')  
        alkohol = self.request.GET.get('alkohol')  
        vegansko = self.request.GET.get('vegansko')  
        min_kolicina = self.request.GET.get('min_kolicina')  


        if search:
            queryset = queryset.filter(pice_naziv__icontains=search)

        if alkohol:
            if alkohol == 'true':
                queryset = queryset.filter(pice_sadrzi_alkohol=True)
            elif alkohol == 'false':
                queryset = queryset.filter(pice_sadrzi_alkohol=False)

        if vegansko:
            if vegansko == 'true':
                queryset = queryset.filter(pice_vegansko=True)
            elif vegansko == 'false':
                queryset = queryset.filter(pice_vegansko=False)
        
        if min_kolicina:
            queryset = queryset.filter(pice_kolicina_u_ml__gte=min_kolicina)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


def dodaj_pice(request):
    if request.method == 'POST':
        form = PiceForm(request.POST)
        if form.is_valid():
            form.save() 
            return redirect('main:drink_list_view') 
    else:
        form = PiceForm()
    
    return render(request, 'main/admin/lista_pica/dodavanje_pica/add_drink.html', {'form': form})



class PiceDetailView(DetailView):
    model = Pice
    template_name = 'main/admin/lista_pica/pregled_pica/detail_view.html'  
    context_object_name = 'pice'  



# slijedeci list view je view iz sucelja konobara, konobar pristupa svojim narudzbama

class NarudzbaListView(ListView):
    model = Narudzba
    template_name = 'main/user/lista_narudzbi/list_view.html'
    context_object_name = 'narudzbe'
    paginate_by = 10 

    def get_queryset(self):
        queryset = super().get_queryset()

        user = self.request.user

        if not user.is_authenticated:
            return queryset.none()

        queryset = queryset.filter(narudzba_konobar=user)
        
        placena_filter = self.request.GET.get('placena')

        if placena_filter is not None and placena_filter != "":
            queryset = queryset.filter(narudzba_placena=(placena_filter.lower() == 'true'))

        return queryset



@login_required
def kreiraj_narudzbu(request):
   
    nova_narudzba = Narudzba(
        narudzba_kolicina_stavki=0,
        narudzba_konobar=request.user,  
        narudzba_placena=False,
        narudzba_ukupna_cijena=0
    )
    nova_narudzba.save()

  
    return redirect('main:lista_narudzbi')


class NarudzbaDetailView(DetailView):
    model = Narudzba
    template_name = 'main/user/lista_narudzbi/detalji_narudzbe/narudzba_details.html'
    context_object_name = 'narudzba'
    
   
    slug_field = 'narudzba_sifra'
    slug_url_kwarg = 'narudzba_sifra'  

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        narudzba = self.get_object()  
        context['stavke'] = StavkaNarudzbe.objects.filter(stavka_narudzba=narudzba)
        context['form'] = StavkaNarudzbeForm()  
        return context

    def post(self, request, *args, **kwargs):
        
        narudzba = self.get_object()

       
        if 'plati' in request.POST:
            narudzba.narudzba_placena = True

            for stavka in narudzba.stavke.all():
                narudzba.narudzba_ukupna_cijena += stavka.stavka_ukupna_cijena

            konobar = narudzba.narudzba_konobar.konobar
            konobar.konobar_zarada += narudzba.narudzba_ukupna_cijena

            narudzba.save()
            konobar.save()

            return redirect('main:detalji_narudzbe', narudzba_sifra=narudzba.narudzba_sifra)

      
        elif 'dodaj_stavku' in request.POST:
            form = StavkaNarudzbeForm(request.POST)
            if form.is_valid():
              
                nova_stavka = form.save(commit=False)
                nova_stavka.stavka_narudzba = narudzba
                nova_stavka.save()
            
           
            return redirect('main:detalji_narudzbe', narudzba_sifra=narudzba.narudzba_sifra)

        return super().post(request, *args, **kwargs)


class StavkaNarudzbeDetailView(DetailView):
    model = StavkaNarudzbe
    template_name = 'main/user/lista_narudzbi/detalji_narudzbe/detalji_stavke_narudzbe/detail_view.html'
    context_object_name = 'stavka'


class KonobarDetailView(LoginRequiredMixin, DetailView):
    model = Konobar
    template_name = 'main/user/podaci_korisnika/detailView.html'
    context_object_name = 'konobar'

    def get_object(self, queryset=None):
       
        return self.request.user.konobar

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user 
        return context



class KonobarListViewFromAdmin(ListView):
    model = Konobar
    template_name = 'main/admin/lista_konobara/konobar_list_view.html' 
    context_object_name = 'konobari'

    def get_queryset(self):
        queryset = super().get_queryset()

        # Uzmi parametar 'search' iz GET zahteva
        search_query = self.request.GET.get('search', '')

        if search_query:
            # Filtriraj queryset na osnovu 'search_query'
            queryset = queryset.filter(
                Q(konobar_ime__icontains=search_query) |  # Pretraga po imenu konobara
                Q(user__username__icontains=search_query)  # Pretraga po username-u korisnika
            )
        
        return queryset


class KonobarDetailViewFromAdmin(DetailView):
    model = Konobar
    template_name = 'main/admin/lista_konobara/detalji_konobara/detail_view.html'  
    context_object_name = 'konobar'

    def get_object(self):
    
        return Konobar.objects.get(user__pk=self.kwargs['user_pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        konobar = self.get_object()
        context['narudzbe'] = konobar.user.narudzbe.all()
        return context

class NarudzbaDetailViewFromAdmin(DetailView):
    model = Narudzba
    template_name = 'main/admin/lista_konobara/detalji_konobara/detalji_narudzbe/detail_view.html'
    context_object_name = 'narudzba'

    def get_object(self):
       
        return Narudzba.objects.get(narudzba_sifra=self.kwargs['narudzba_sifra'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        narudzba = self.get_object()
        context['stavke'] = narudzba.stavke.all()  
        return context

"""
def detalji_narudzbe(request, narudzba_sifra):
    # Dohvati narudžbu prema šifri
    narudzba = get_object_or_404(Narudzba, narudzba_sifra=narudzba_sifra)
    
    # Dohvati sve stavke za ovu narudžbu
    stavke = StavkaNarudzbe.objects.filter(stavka_narudzba=narudzba)
    
    if request.method == 'POST':
        # Ako je kliknuto na gumb "Plati", ažuriraj narudžbu
        if 'plati' in request.POST:
            narudzba.narudzba_placena = True
            narudzba.save()
            return redirect('main:detalji_narudzbe', narudzba_sifra=narudzba.narudzba_sifra)  

    return render(request, 'main/user/lista_narudzbi/detalji_narudzbe/narudzba_details.html', {
        'narudzba': narudzba,
        'stavke': stavke
    })



def kreiraj_narudzbu(request):
    # Formset za dodavanje više stavki odjednom
    StavkaFormSet = inlineformset_factory(
        Narudzba,
        StavkaNarudzbe,
        form=StavkaNarudzbeForm,
        extra=1,
        can_delete=True
    )

    if request.method == 'POST':
        narudzba_form = NarudzbaForm(request.POST)
        if narudzba_form.is_valid():
            narudzba = narudzba_form.save(commit=False)
            narudzba.narudzba_konobar = request.user
            narudzba.save()

            formset = StavkaFormSet(request.POST, instance=narudzba)
            if formset.is_valid():
                formset.save()

                # Ažuriraj broj stavki
                narudzba.narudzba_kolicina_stavki = narudzba.stavke.count()
                narudzba.save()

                return redirect('lista_narudzbi')
            else:
                # Ako formset nije validan, obriši kreiranu narudžbu
                narudzba.delete()
        else:
            # Ako forma za narudžbu nije validna, samo prosledi prazan formset
            formset = StavkaFormSet()
    else:
        narudzba_form = NarudzbaForm()
        formset = StavkaFormSet()

    return render(request, 'main/user/lista_narudzbi/kreiranje_narudzbe/kreiranje_narudzbe.html', {
        'narudzba_form': narudzba_form,
        'formset': formset,
    })
"""