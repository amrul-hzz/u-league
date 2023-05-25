from django.urls import path
from .views import *

urlpatterns = [
    path('', get_all_pertandingan, name='semua_pertandingan'),
    path('pilih_pertandingan/', select_pertandingan, name='pilih_pertandingan'),
    path('buat_pertandingan/<str:row_id>', create_pertandingan, name='buat_pertandingan'),
    path('delete_pertandingan/<str:row_id>', delete_pertandingan, name='delete_pertandingan'),
]
