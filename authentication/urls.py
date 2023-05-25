from django.urls import path
from authentication.views import *

app_name = 'authentication'

urlpatterns = [
    path('login/', login, name='login'),
    path('logout/', logout_view, name='logout'),
    path('landing/', landing, name='landing'),
    path('landing-register/', landing_register, name='landing-register'),
    path('register_manajer/', register_manajer, name='register_manajer'),
    path('create_manajer/', create_manajer, name="create_manajer"),
    path('register_penonton/', register_penonton, name='register_penonton'),
    path('create_penonton/', create_penonton, name="create_penonton"),

]