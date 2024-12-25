from django.urls import path
from . import views

app_name = 'main' 

urlpatterns = [

    path('', views.homepage, name='homepage'),   
    path('manage-users/', views.manage_users, name='manage_users'),
    path('register/', views.register, name='register'), 
    path('register-super-user', views.register_superuser, name='register_superuser')
]


urlpatterns += [
    path('edit-user/<int:user_id>/', views.edit_user, name='edit_user'),
    path('delete-user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('add-user/', views.add_user, name='add_user'),
    path('add_admin/', views.add_admin, name='add_admin'),
    path('add_konobar/', views.add_konobar, name='add_konobar'),
    path('show-other-users/', views.show_other_users, name='show_other_users'),
    path('lista-pica', views.PiceListView.as_view(), name='drink_list_view'),
    path('dodaj-pice/', views.dodaj_pice, name='dodaj_pice'),
    path('pice/<int:pk>/', views.PiceDetailView.as_view(), name='pice_detail'),
    path('lista-narudzbi/', views.NarudzbaListView.as_view(), name='lista_narudzbi'),
    path('kreiraj-narudzbu/', views.kreiraj_narudzbu, name='kreiraj_narudzbu'),
    path('detalji_narudzbe/<uuid:narudzba_sifra>/', views.NarudzbaDetailView.as_view(), name='detalji_narudzbe'),
    path('stavka_narudzbe/<uuid:pk>/', views.StavkaNarudzbeDetailView.as_view(), name='stavka_narudzbe'),
    path('konobar/detalji/', views.KonobarDetailView.as_view(), name='konobar_detalji'),

    path('konobari/',views.KonobarListViewFromAdmin.as_view(), name='konobar_list_view'),
    path('konobar/<int:user_pk>/', views.KonobarDetailViewFromAdmin.as_view(), name='konobar_detail'),
    path('narudzbaFromAdmin/<uuid:narudzba_sifra>/', views.NarudzbaDetailViewFromAdmin.as_view(), name='narudzba_detail'),
    
]


urlpatterns += [

    path('<uuid:pk>/update/', views.PiceUpdateView.as_view(), name='drink_update_view'),
    path('<uuid:pk>/delete/', views.PiceDeleteView.as_view(), name='drink_delete_view'),
    path('narudzba/<uuid:narudzba_sifra>/delete/', views.NarudzbaDeleteView.as_view(), name='narudzba_delete_view'),
    path('stavka_narudzbe/<uuid:stavka_sifra>/delete/', views.StavkaNarudzbeDeleteView.as_view(), name='stavka_delete_view'),



]

