from django.urls import path
from dashboard.views import *

app_name = 'dashboard'

urlpatterns = [
    path('penonton/', show_dashboard_penonton, name='show_dashboard_penonton'),
]
