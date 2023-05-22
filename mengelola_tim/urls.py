from django.urls import path
from .views import pendaftaran_tim, tim, daftar_pemain, daftar_pelatih

app_name = 'mengelolatim'

urlpatterns = [
    path('', pendaftaran_tim, name='pendaftaran_tim'),
    path('tim/', tim, name='tim'),
    path('daftarpemain/', daftar_pemain, name='daftar_pemain'),
    path('daftarpelatih/', daftar_pelatih, name='daftar_pelatih'),
]