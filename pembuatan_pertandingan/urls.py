from django.urls import path
from .views import get_semua_pertandingan, get_avail_stadium, get_all_wasit, delete_pertandingan

urlpatterns = [
    path('semua_pertandingan/', get_semua_pertandingan, name='semua_pertandingan'),
    path('buat_pertandingan/', get_avail_stadium, name='buat_pertandingan'),
    path('submit_pertandingan/', get_all_wasit, name='submit_pertandingan'),
    path('delete_pertandingan/<str:row_id>', delete_pertandingan, name='delete_pertandingan'),
]
