from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.db import connection

def get_semua_pertandingan(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM PERTANDINGAN")
        data = cursor.fetchall()
    
    # Process the retrieved data as per your needs
    # For example, you can convert it to a list of dictionaries
    result = []
    for i in range(len(data)):
        result.append(
            data[i]
        )

    return JsonResponse(result, safe=False)

def is_panitia(request, id):
    # Implementasikan logika untuk mengecek apakah user adalah panitia
    # Misalnya, Anda dapat menggunakan perintah request.user.groups.filter(name='panitia').exists()
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM PANITIA WHERE ID = %s", [id])
        data = cursor.fetchall()

    if data != null:
        return True
    else:
        return False


def buat_pertandingan(request, id):
    if is_panitia(id):
        # validate jadwal tim dan wasit sebelum mebuat pertandingan
        return true

def validate_jadwal_tim(value):
    pertandingan = Pertandingan.objects.filter(waktu=value)
