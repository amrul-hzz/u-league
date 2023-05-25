from django.urls import path
from mulai_pertandingan.views import *

app_name = 'mulai_pertandingan'

urlpatterns = [
    path('mulai-pertandingan/<uuid:id_pertandingan>/', show_mulai_pertandingan, name='show_mulai_pertandingan'),
    path('mulai-pertandingan/<uuid:id_pertandingan>/pilih-peristiwa/<str:nama_tim>/', show_pilih_peristiwa, name='show_pilih_peristiwa'),
    # path('mulai', show_mulai_pertandingan, name='show_mulai_pertandingan'),
    # path('pilih2', show_pilih_peristiwa2, name='show_pilih_peristiwa2'),
]