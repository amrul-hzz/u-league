from django.urls import path
from peminjaman_stadium.views import  *
app_name = "peminjaman_stadium"

urlpatterns = [
    path('', list_pemesanan, name='list_pemesanan'),
    path('pilih_stadium/', pilih_stadium, name='pilih_stadium'),
    path('add_pemesanan/', add_pemesanan, name='add_pemesanan'),
    # path('list_waktu/', list_waktu, name='list_waktu'),
]