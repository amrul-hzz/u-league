from django.urls import path
from .views import *

app_name = 'list_pertandingan'

urlpatterns = [
    path('', list_pertandingan, name='list_pertandingan'),
    path('list_pertandingan/', list_pertandingan, name='list_pertandingan')
]