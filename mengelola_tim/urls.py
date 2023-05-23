from django.urls import path
from .views import tim, daftar_pemain, daftar_pelatih, create_tim, get_tim

app_name = 'mengelolatim'

urlpatterns = [
    path('', get_tim, name='tim'),
    path('daftar_pemain/', daftar_pemain, name='daftar_pemain'),
    path('daftar_pelatih/', daftar_pelatih, name='daftar_pelatih'),
    path('create_tim/', create_tim, name='create_tim'),
]