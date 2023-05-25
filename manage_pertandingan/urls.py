from django.urls import path
from manage_pertandingan.views import *

app_name = 'manage_pertandingan'

urlpatterns = [
    path('', show_manage_pertandingan, name='show_manage_pertandingan'),
    path('peristiwa-tim/<uuid:id_pertandingan>/<str:nama_tim>/', show_lihat_peristiwa, name='show_lihat_peristiwa'),
    # path('stage', show_list_pertandingan_stage, name='list-pertandingan-stage'),
    # path('nonstage', show_list_pertandingan_nonstage, name='list-pertandingan-nonstage'),
    # path('akhir', show_manage_pertandingan_sesudah, name='manage-pertandingan-sesudah'),
    # path('lihat-peristiwa', show_lihat_peristiwa, name='show-lihat-peristiwa'),
]