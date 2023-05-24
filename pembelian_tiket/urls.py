from django.urls import path
from .views import *

app_name = 'pembelian_tiket'

urlpatterns = [
    path('', pilih_stadium, name='pilih_stadium'),
    path('pilih_stadium/', pilih_stadium, name='pilih_stadium'),
    path('list_waktu_dan_pertandingan/', list_waktu_dan_pertandingan, name='list_waktu_dan_pertandingan'),
    path('beli_tiket/<UUID:id_pertandingan', beli_tiket, name='beli_tiket'),
]