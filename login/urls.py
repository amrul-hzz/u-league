from django.urls import path
from login.views import login

app_name = 'login'

urlpatterns = [
    path('', login, name='login'),
]