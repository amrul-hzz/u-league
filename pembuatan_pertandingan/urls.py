from django.urls import path
from .views import get_all_wasit_tim, get_all_pertandingan, delete_pertandingan, create_pertandingan

urlpatterns = [
    path('', get_all_pertandingan, name='semua_pertandingan'),
    path('buat_pertandingan/<str:row_id>/', get_all_wasit_tim, name='buat_pertandingan'),
    path('submit_pertandingan/<str:row_id>/', create_pertandingan, name='submit_pertandingan'),
    path('delete_pertandingan/<str:row_id>/', delete_pertandingan, name='delete_pertandingan'),
]
