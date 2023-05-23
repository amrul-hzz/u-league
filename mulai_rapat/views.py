from django.shortcuts import render
from django.shortcuts import render
import datetime
from django.db import connection
import uuid
from django.http import HttpResponseRedirect

# Create your views here.
def pilih_pertandingan(request):
    return render(request, "pilih_pertandingan.html")

def rapat_pertandingan(request):
    return render(request, "rapat_pertandingan.html")


