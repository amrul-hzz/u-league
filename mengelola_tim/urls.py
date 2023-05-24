from django.urls import path
from .views import *

app_name = 'mengelolatim'

urlpatterns = [
    path('', get_tim, name='tim'),
    path('daftar_pemain/', show_pemain_null, name='show_pemain_null'),
    path('daftar_pelatih/', show_pelatih_null, name='daftar_pelatih'),
    path('create_tim/', create_tim, name='create_tim'),
    path('make_captain/<str:id>', make_captain, name='make_captain'),
    path('delete_pemain/<str:id>', delete_pemain, name='delete_pemain'),
    path('delete_pelatih/<str:id>', delete_pelatih, name='delete_pelatih'),
    path('show_pemain_null/<str:id>', show_pemain_null, name='show_pemain_null'),
    path('add_pemain/', add_pemain, name='add_pemain'),
    path('show_pelatih_null/', show_pelatih_null, name='show_pelatih_null'),
    # path('add_pelatih/', add_pelatih, name='add_pelatih'),
]