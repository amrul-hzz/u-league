from django.urls import path
from authentication.views import *

app_name = 'authentication'

urlpatterns = [
    path('login/', login, name='login'),
    path('logout/', logout_view, name='logout'),
    path('landing/', landing, name='landing'),
    path('landing-register/', landing_register, name='landing-register'),

    # path ke form registrasi penonton
    # path('show_register_penonton', show_register_penonton, name='show_register_penonton'),
    # path('dashboard/dashboard_penonton/', show_dashboard_penonton, name='show_dashboard_penonton'),

    path('register_manajer/', register_manajer, name='register_manajer'),
    path('create_manajer/', create_manajer, name="create_manajer"),

]