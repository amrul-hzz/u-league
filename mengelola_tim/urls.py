from django.urls import path
from .views import pendaftaran_tim, tim, daftar_pemain, daftar_pelatih

app_name = 'mengelolatim'

urlpatterns = [
    path('pendaftaran_tim', pendaftaran_tim, name='pendaftaran_tim'),
    path('', tim, name='tim'),
    path('daftar_pemain/', daftar_pemain, name='daftar_pemain'),
    path('daftar_pelatih/', daftar_pelatih, name='daftar_pelatih'),
]