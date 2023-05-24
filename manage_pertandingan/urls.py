from django.urls import path
from manage_pertandingan.views import *

app_name = 'manage_pertandingan'

urlpatterns = [
    path('sebelum', show_manage_pertandingan_sebelum, name='manage-pertandingan-sebelum'),
    path('stage', show_list_pertandingan_stage, name='list-pertandingan-stage'),
    path('nonstage', show_list_pertandingan_nonstage, name='list-pertandingan-nonstage'),
    path('akhir', show_manage_pertandingan_sesudah, name='manage-pertandingan-sesudah'),
    path('lihat-peristiwa', show_lihat_peristiwa, name='show-lihat-peristiwa'),
]