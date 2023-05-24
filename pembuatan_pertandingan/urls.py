from django.urls import path
from .views import get_semua_pertandingan, get_avail_stadium

urlpatterns = [
    path('semua_pertandingan/', get_semua_pertandingan, name='semua_pertandingan'),
    path('buat_pertandingan/', get_avail_stadium, name='buat_pertandingan'),

]
