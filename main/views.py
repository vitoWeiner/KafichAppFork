from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group  # Dodano
from .forms import *
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from .models import *
from django.db.models import Q
from django_filters import *
from django.urls import reverse_lazy

from django.forms import inlineformset_factory
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import update_session_auth_hash


from main.serializers import PiceSerializer
from rest_framework import viewsets

from rest_framework.permissions import IsAuthenticated

import requests

from django.shortcuts import render

from requests.auth import HTTPBasicAuth



class PiceViewSet(viewsets.ModelViewSet):
    queryset = Pice.objects.all().order_by('pice_naziv')
    serializer_class = PiceSerializer
    permission_classes = [IsAuthenticated]  
    lookup_field = 'pice_sifra'  


@login_required
def pica_list_view_REST(request):


    if request.user.is_authenticated:
        session = requests.Session()
        session.cookies.update(request.COOKIES)
        response = session.get('http://localhost:8000/RESTfulAPI/pica_restful/')

        if response.status_code == 200:
            pica_data = response.json()  
        
        else:
            pica_data = []
        
        return render(request, 'main/admin/lista_pica_REST/list_view.html', {'pica_data': pica_data})

    else:
        pica_data = []
        return render(request, 'main/admin/lista_pica_REST/list_view.html', {'pica_data': pica_data})



    response = requests.get('http://localhost:8000/RESTfulAPI/pica_restful/')

    if response.status_code == 200:
        pica_data = response.json()  
    else:
        pica_data = []

    return render(request, 'main/admin/lista_pica_REST/list_view.html', {'pica_data': pica_data})








@login_required
def pica_update_view(request, pice_sifra):

    if request.user.is_authenticated:

        session = requests.Session()
        session.cookies.update(request.COOKIES)

        if request.method == 'GET':

    # Dohvaćanje pića putem REST API-ja
            response = session.get(f'http://localhost:8000//RESTfulAPI/pica_restful/{pice_sifra}/')

            print ('posted')
    
            if response.status_code == 200:
                pice_data = response.json()
            else:
                return HttpResponse(f"Piće nije pronađeno {response.status_code} ", status=response.status_code)

        elif request.method == 'POST':

            # session = requests.Session()
            # session.cookies.update(request.COOKIES)

            print('geted')

            if request.user.is_authenticated:
                print (session)

            # session = requests.Session()


            update_data = {
                'pice_sifra' : str(pice_sifra),
                'pice_naziv': request.POST.get('pice_naziv'),
                'pice_opis': request.POST.get('pice_opis'),
                'pice_kolicina_u_ml': request.POST.get('pice_kolicina_u_ml'),
                'pice_sadrzi_alkohol': request.POST.get('pice_sadrzi_alkohol') == 'on',
                'pice_vegansko': request.POST.get('pice_vegansko') == 'on',
                'pice_poj_cijena': request.POST.get('pice_poj_cijena'),
            }

            update_response = session.patch(
                f'http://localhost:8000/RESTfulAPI/pica_restful/{pice_sifra}/', 
                json = update_data,
                headers={'X-CSRFToken': request.COOKIES['csrftoken']}

            )

            if update_response.status_code == 200:
                return redirect('main:pica_list_view_REST')  # Preusmjeri nakon ažuriranja
            else:
                return HttpResponse(f"Greška pri ažuriranju podataka{update_response.status_code}", status=update_response.status_code)

        return render(request, 'main/admin/lista_pica_REST/update_form_REST/update_pice.html', {'pice': pice_data})


@login_required
def pica_delete_view(request, pice_sifra):
    if request.user.is_authenticated:
        session = requests.Session()
        session.cookies.update(request.COOKIES)
        delete_response = session.delete(
            f'http://localhost:8000/RESTfulAPI/pica_restful/{pice_sifra}/',
            headers={'X-CSRFToken': request.COOKIES['csrftoken']}
        )

        if delete_response.status_code == 204:
            return redirect('main:pica_list_view_REST')  # Preusmjeri nakon brisanja
        else:
            return HttpResponse(f"Greška pri brisanju podataka {delete_response.status_code}", status=delete_response.status_code)


@login_required
def pica_create_view(request):

    if request.user.is_authenticated:

        session = requests.Session()
        session.cookies.update(request.COOKIES)

        if request.method == 'POST':
            create_data = {
                'pice_naziv': request.POST.get('pice_naziv'),
                'pice_opis': request.POST.get('pice_opis'),
                'pice_kolicina_u_ml': request.POST.get('pice_kolicina_u_ml'),
                'pice_sadrzi_alkohol': request.POST.get('pice_sadrzi_alkohol') == 'on',
                'pice_vegansko': request.POST.get('pice_vegansko') == 'on',
                'pice_poj_cijena': request.POST.get('pice_poj_cijena'),
            }

            create_response = session.post(
                'http://localhost:8000/RESTfulAPI/pica_restful/',
                json=create_data,
                headers={'X-CSRFToken': request.COOKIES['csrftoken']}
            )

            if create_response.status_code == 201:
                return redirect('main:pica_list_view_REST')  # Preusmjeri nakon stvaranja
            else:
                return HttpResponse(f"Greška pri stvaranju podataka {create_response.status_code}", status=create_response.status_code)

        return render(request, 'main/admin/lista_pica_REST/create_form_REST/add_pice.html')



 ## ## # from django.contrib.auth.models import User

## Create your views here.


#homepage od korisnika i od admina

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



 
# funkcijonalnost za registriranje novog korisnika (konobara)
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




# funkcijonalnost za registriranje novog admina

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


            return redirect('login')  
    else:
        form = UserCreationForm()

    return render(request, 'registration/register_super_user.html', {'form': form})



# funkcijonalnost kojoj se pristupa iz sucelja admina:
# admin pomocu ove funkcijonalnosti moze pregledavati i uredivati podatke trenutnih korisnika, ili dodavati nove korisnike

@login_required
def manage_users(request):
    if request.user.groups.filter(name='Korisnik').exists():
        return redirect('main:homepage')  

    query = request.GET.get('q')  

    if query:
        users = User.objects.filter(username__icontains=query)  
    else:
        users = User.objects.all()  

    return render(request, 'main/admin/upravljanje_korisnicima/manage_users.html', {'users': users})



# funkcijonalnost kojoj se pristupa iz sucelja admina:
# admin pomocu ove funkcijonalnosti ureduje podatke nekog korisnika

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


# funkcijonalnost kojoj se pristupa iz sucelja admina:
# admin pomocu ove funkcijonalnosti brise postojeceg korisnika

@login_required
def delete_user(request, user_id):
    if request.user.groups.filter(name='Korisnik').exists():
        return redirect('main:homepage')

    user = User.objects.get(id=user_id)
    if request.method == 'POST':
        user.delete()
        return redirect('main:manage_users')

    return render(request, 'main/admin/upravljanje_korisnicima/brisanje_korisnika/delete_user.html', {'user': user})


# funkcijonalnost kojoj se pristupa iz sucelja admina:
# admin pomocu ove funkcijonalnosti dodaje novog korisnika

@login_required
def add_user(request):
    
    #if not request.user.groups.filter(name='Korisnik').exists():
    return render(request, 'main/admin/upravljanje_korisnicima/dodavanje_novog_korisnika/add_user.html')
    #else:
     #   return redirect('main:homepage')



# funkcijonalnost kojoj se pristupa iz sucelja admina:
# admin pomocu ove funkcijonalnosti dodaje novog admina 

def add_admin(request):
    if request.method == 'POST':
        form = AdminCreationForm(request.POST)
        if form.is_valid():
            form.save()  
            return redirect('main:manage_users')
    else:
        form = AdminCreationForm()

    return render(request, 'main/admin/upravljanje_korisnicima/dodavanje_novog_korisnika/dodavanje_novog_administratora/add_admin.html', {'form': form})


# funkcijonalnost kojoj se pristupa iz sucelja admina:
# admin pomocu ove funkcijonalnosti dodaje novog korisnika koji je konobar


def add_konobar(request):
    if request.method == 'POST':
        form = KonobarCreationForm(request.POST)
        if form.is_valid():
            form.save() 
            return redirect('main:manage_users')  
    else:
        form = KonobarCreationForm()

    return render(request, 'main/admin/upravljanje_korisnicima/dodavanje_novog_korisnika/dodavanje_novog_Konobara/add_konobar.html', {'form': form})



# funkcijonalnost kojoj se pristupa iz sucelja korisnika (konobara):
# korisnik moze pregledavati podatke ostalih korisnika (ova funkcijonalnost trenutno iskljucena iz UI)


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


# funkcijonalnost kojoj se pristupa iz sucelja admina:
# admin pregledava postojeca pica u bazi podataka i moze dodati nova ako zeli

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



# funkcijonalnost kojoj se pristupa iz sucelja admina:
# admin putem ove funkcije dodaje nova pica

def dodaj_pice(request):
    if request.method == 'POST':
        form = PiceForm(request.POST)
        if form.is_valid():
            form.save() 
            return redirect('main:drink_list_view') 
    else:
        form = PiceForm()
    
    return render(request, 'main/admin/lista_pica/dodavanje_pica/add_drink.html', {'form': form})



# funkcijonalnost kojoj se pristupa iz sucelja admina:
# admin putem ove funkcije pregledava detalje o picima

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

        return queryset.order_by('narudzba_datum_kreiranja')

# konobar putem slijedece funkcije moze kreirati novu narudzbu

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

# konobar putem slijedece funkcije moze vidjeti detalje o odabranoj narudzbi iz listviewa


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

                narudzba.narudzba_kolicina_stavki += 1
                narudzba.save()
            
           
            return redirect('main:detalji_narudzbe', narudzba_sifra=narudzba.narudzba_sifra)

        return super().post(request, *args, **kwargs)


# nakon sto je konobar kliknuo na narudzbu, otvaraju mu se detalji narudzbe. tamo moze dodati stavke narudzbe, kada klikne na stavku otvara mu se detail view za stavku
# detail view za stavku:


class StavkaNarudzbeDetailView(DetailView):
    model = StavkaNarudzbe
    template_name = 'main/user/lista_narudzbi/detalji_narudzbe/detalji_stavke_narudzbe/detail_view.html'
    context_object_name = 'stavka'


# konobar moze pregledavati svoje osobne podatke (ime, prezime, zarada i slicno)

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

# admin takoder ima pristup listi konobara te moze preko nje pristupiti pogledu za sve njihove narudzbe
# ovo je listview s konobarima iz sucelja admina

class KonobarListViewFromAdmin(ListView):
    model = Konobar
    template_name = 'main/admin/lista_konobara/konobar_list_view.html' 
    context_object_name = 'konobari'

    def get_queryset(self):
        queryset = super().get_queryset()

        
        search_query = self.request.GET.get('search', '')

        if search_query:
            
            queryset = queryset.filter(
                Q(konobar_ime__icontains=search_query) |  
                Q(user__username__icontains=search_query) 
            )
        
        return queryset


# detalji o pojedinom konobaru iz sucelja admina 

class KonobarDetailViewFromAdmin(DetailView):
    model = Konobar
    template_name = 'main/admin/lista_konobara/detalji_konobara/detail_view.html'  
    context_object_name = 'konobar'

    def get_object(self):
    
        return Konobar.objects.get(user__pk=self.kwargs['user_pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        konobar = self.get_object()


        filter_status = self.request.GET.get('placeno', None)

        if filter_status == 'true':
            narudzbe = konobar.user.narudzbe.filter(narudzba_placena=True)
        elif filter_status == 'false':
            narudzbe = konobar.user.narudzbe.filter(narudzba_placena=False)
        else:
            narudzbe = konobar.user.narudzbe.all()

        context['narudzbe'] = narudzbe
        return context

# admin moze pristupiti svim narudzbama pojedinog konobara
# slijedeca funkcijonalnost omogucuje pregled detalja svake narudzbe

class NarudzbaDetailViewFromAdmin(DetailView):
    model = Narudzba
    template_name = 'main/admin/lista_konobara/detalji_konobara/detalji_narudzbe/detail_view.html'
    context_object_name = 'narudzba'

    def get_object(self):
       
        return Narudzba.objects.get(narudzba_sifra=self.kwargs['narudzba_sifra'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        narudzba = self.get_object()


        search_pice = self.request.GET.get('search_pice', '')

        if search_pice:
            stavke = narudzba.stavke.filter(
                stavka_pice__pice_naziv__icontains=search_pice
            )

        else:
            stavke = narudzba.stavke.all()



        context['stavke'] = stavke
        return context



class PiceUpdateView(UpdateView):
    model = Pice
    fields = ['pice_naziv', 'pice_opis', 'pice_kolicina_u_ml', 'pice_sadrzi_alkohol', 'pice_vegansko', 'pice_poj_cijena']
    template_name = 'main/admin/lista_pica/pregled_pica/uredivanje_pica/edit_drink_form.html'

    def get_object(self, queryset=None):
     
        return get_object_or_404(Pice, pice_sifra=self.kwargs['pk'])

    def get_success_url(self):
        return reverse_lazy('main:pice_detail', kwargs={'pk': self.object.pk})



class PiceDeleteView(DeleteView):
    model = Pice
    template_name = 'main/admin/lista_pica/pregled_pica/brisanje_pica/drink_confirm_delete.html'
    success_url = reverse_lazy('main:drink_list_view')

    def get_object(self, queryset=None):

        return get_object_or_404(Pice, pice_sifra=self.kwargs['pk'])



class NarudzbaDeleteView(DeleteView):
    model = Narudzba
    template_name = 'main/user/lista_narudzbi/detalji_narudzbe/brisanje_narudzbe/confirm_delete.html' 
    context_object_name = 'narudzba'
    success_url = reverse_lazy('main:lista_narudzbi') 

    def get_object(self, queryset=None):

        return Narudzba.objects.get(narudzba_sifra=self.kwargs['narudzba_sifra'])


class StavkaNarudzbeDeleteView(DeleteView):
    model = StavkaNarudzbe
    template_name = 'main/user/lista_narudzbi/detalji_narudzbe/detalji_stavke_narudzbe/brisanje_stavke_narudzbe/confirm_delete.html' 
    context_object_name = 'stavka'
    
    def get_success_url(self):
        
        return reverse_lazy('main:detalji_narudzbe', kwargs={'narudzba_sifra': self.object.stavka_narudzba.narudzba_sifra})

    def get_object(self, queryset=None):
   
        return StavkaNarudzbe.objects.get(stavka_sifra=self.kwargs['stavka_sifra'])

    def delete(self, request, *args, **kwargs):

        
   
        stavka = self.get_object()


        
  
        narudzba = stavka.stavka_narudzba
        narudzba.narudzba_kolicina_stavki -= 1
        narudzba.save()

     
        return super().delete(request, *args, **kwargs)


class StavkaNarudzbeUpdateView(UpdateView):
    model = StavkaNarudzbe
    form_class = StavkaNarudzbeForm
    template_name = 'main/user/lista_narudzbi/detalji_narudzbe/detalji_stavke_narudzbe/azuriranje_stavke/azuriranje_stavke.html'

    def form_valid(self, form):
       
        self.object = form.save(commit=False)
    
        self.object.stavka_ukupna_cijena = self.object.stavka_kolicina_pica * self.object.stavka_pice.pice_poj_cijena
        self.object.save()
        return super().form_valid(form)

    def get_success_url(self):
   
        return reverse_lazy('main:stavka_narudzbe', kwargs={'pk': self.object.stavka_sifra})



# KonobarUpdateView

class KonobarUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'main/user/podaci_korisnika/azuriranje_korisnika/update_view.html'

    def get(self, request, *args, **kwargs):
        user_form = UserForm(instance=request.user)
        konobar_form = KonobarForm(instance=request.user.konobar)
        return render(request, self.template_name, {'user_form': user_form, 'konobar_form': konobar_form})

    def post(self, request, *args, **kwargs):
        user_form = UserForm(request.POST, instance=request.user)
        konobar_form = KonobarForm(request.POST, instance=request.user.konobar)

        if user_form.is_valid() and konobar_form.is_valid():
           
            user = user_form.save(commit=False) 



            user.save()  
            konobar_form.save() 


            return redirect('main:konobar_detalji')

        return render(request, self.template_name, {'user_form': user_form, 'konobar_form': konobar_form})


class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'main/user/podaci_korisnika/brisanje_korisnika/delete_view.html'
    success_url = reverse_lazy('main:homepage') 

    def get_object(self, queryset=None):
    
        return self.request.user

"""
def detalji_narudzbe(request, narudzba_sifra):

    narudzba = get_object_or_404(Narudzba, narudzba_sifra=narudzba_sifra)
    

    stavke = StavkaNarudzbe.objects.filter(stavka_narudzba=narudzba)
    
    if request.method == 'POST':

        if 'plati' in request.POST:
            narudzba.narudzba_placena = True
            narudzba.save()
            return redirect('main:detalji_narudzbe', narudzba_sifra=narudzba.narudzba_sifra)  

    return render(request, 'main/user/lista_narudzbi/detalji_narudzbe/narudzba_details.html', {
        'narudzba': narudzba,
        'stavke': stavke
    })



def kreiraj_narudzbu(request):

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