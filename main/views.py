from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group  # Dodano
from .forms import *
from django.views.generic import ListView, DetailView
from .models import *

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
        form = UserCreationForm(request.POST)  
        if form.is_valid():  
            user = form.save()  

            group = Group.objects.get(name='Korisnik')  
            group.user_set.add(user)  


            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password) 
            login(request, user) 
            return redirect('main:homepage') 
    else:
        form = UserCreationForm()  

    context = {'form': form}
    return render(request, 'registration/register.html', context)



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
    if not request.user.groups.filter(name='Korisnik').exists():  
        if request.method == 'POST':
            form = UserCreationWithGroupForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('main:manage_users') 
        else:
            form = UserCreationWithGroupForm()  

        return render(request, 'main/admin/upravljanje_korisnicima/dodavanje_novog_korisnika/add_user.html', {'form': form}) 
    else:
        return redirect('main:homepage') 


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

        alkohol = self.request.GET.get('alkohol')  
        vegansko = self.request.GET.get('vegansko')  
        min_kolicina = self.request.GET.get('min_kolicina')  

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