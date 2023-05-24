from django.urls import path
from .views import get_semua_pertandingan, batalkan_peminjaman

urlpatterns = [
    path('batalkan/<waktu>/<stadium>/', batalkan_peminjaman, name='batalkan_peminjaman'),
    path('semua_pertandingan/', get_semua_pertandingan, name='get_semua_pertandingan'),
]
