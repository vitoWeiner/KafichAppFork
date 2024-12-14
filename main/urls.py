from django.urls import path
from . import views

app_name = 'main'  # here for namespacing of urls.

urlpatterns = [

    path('', views.homepage, name='homepage'),   # name = 'homepage' je referenca na url, kako bi se moglo pozvati iz html predlozaka bez da se pise cijeli url
    path('manage-users/', views.manage_users, name='manage_users'),
    path('register/', views.register, name='register'), 
]


urlpatterns += [
    path('edit-user/<int:user_id>/', views.edit_user, name='edit_user'),
    path('delete-user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('add-user/', views.add_user, name='add_user'),
    path('show-other-users/', views.show_other_users, name='show_other_users'),
    path('lista-pica', views.PiceListView.as_view(), name='drink_list_view'),
    path('dodaj-pice/', views.dodaj_pice, name='dodaj_pice'),
    path('pice/<int:pk>/', views.PiceDetailView.as_view(), name='pice_detail'),
]

