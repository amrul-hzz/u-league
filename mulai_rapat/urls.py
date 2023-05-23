from django.urls import path
from mulai_rapat.views import *
app_name = "mulai_rapat"

urlpatterns = [
    path('', pilih_pertandingan, name=''),
    path('rapat_pertandingan/<str:pertandingan>/', rapat_pertandingan, name='rapat_pertandingan'),
]