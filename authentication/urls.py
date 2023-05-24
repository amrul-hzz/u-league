from django.urls import path
from authentication.views import *

app_name = 'authentication'

urlpatterns = [
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('landing/', landing, name='landing'),
    path('landing-register/', landing_register, name='landing-register')
]