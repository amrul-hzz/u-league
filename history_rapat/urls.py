from django.urls import path
from .views import *

app_name = 'history_rapat'

urlpatterns = [
    path('', history_rapat, name='history_rapat'),
    path('history_rapat/', history_rapat, name='history_rapat')
]