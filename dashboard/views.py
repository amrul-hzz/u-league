from django.shortcuts import render
from django.http import JsonResponse
from django.db import connection

# Create your views here.
def show_dashboard(request):
    return render(request, "dashboard_manajer.html")

def show_dashboard_manajer(request):
    return render(request, 'dashboard_manajer.html')

def show_dashboard_panitia(request):
    return render(request, 'dashboard_panitia.html')

