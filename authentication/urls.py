from django.urls import path
from authentication.views import *

app_name = 'authentication'

urlpatterns = [
    path('login/', login, name='login'),
    path('landing/', landing, name='landing'),
    path('landing-register/', landing_register, name='landing-register'),
    # path ke form registrasi penonton
    path('show_register_penonton', show_register_penonton, name='show_register_penonton'),
    path('dashboard/dashboard_penonton/', show_dashboard_penonton, name='show_dashboard_penonton'),
]