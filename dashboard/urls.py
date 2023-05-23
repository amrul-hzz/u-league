from django.urls import path
from .views import *

app_name = 'mengelolatim'

urlpatterns = [
    path('', show_dashboard_manajer, name='show_dashboard_manajer'),
    path('dashboard_penonton/', show_dashboard_penonton, name='show_dashboard_penonton'),
    path('dashboard_manajer/', show_dashboard_manajer, name='show_dashboard_manajer'),
    path('dashboard_panitia/', show_dashboard_panitia, name='show_dashboard_panitia'),
]
