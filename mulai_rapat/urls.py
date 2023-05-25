from django.urls import path
from mulai_rapat.views import *
app_name = "mulai_rapat"

urlpatterns = [
    path('', mulai_rapat, name=''),
    path('rapat_pertandingan/<str:tim1>/<str:tim2>/', rapat_pertandingan, name='rapat_pertandingan'),
    # path('create_rapat/>', create_rapat, name='create_rapat'),
]