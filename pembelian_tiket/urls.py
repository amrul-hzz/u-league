from django.urls import path
from .views import *

app_name = 'pembelian_tiket'

urlpatterns = [
    path('', pilih_stadium, name='pilih_stadium'),
    path('pilih_stadium/', pilih_stadium, name='pilih_stadium'),
    path('list_waktu_dan_pertandingan/', list_waktu_dan_pertandingan, name='list_waktu_dan_pertandingan'),
    path('beli_tiket/<str:id_pertandingan>/', beli_tiket, name='beli_tiket'),
    path('create_pembelian_tiket/<str:id_pertandingan>/', create_pembelian_tiket, name='create_pembelian_tiket'),
]