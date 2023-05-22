from django.shortcuts import render

# Create your views here.
def pendaftaran_tim(request):
    return render(request, "pendaftaran_tim.html")

def tim(request):
    return render(request, "tim.html")

def daftar_pemain(request):
    return render(request, "daftar_pemain.html")

def daftar_pelatih(request):
    return render(request, "daftar_pelatih.html")