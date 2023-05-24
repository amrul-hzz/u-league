from django.urls import path
from .views import get_semua_pertandingan

urlpatterns = [
    path('semua_pertandingan/', get_semua_pertandingan, name='get_semua_pertandingan'),
]