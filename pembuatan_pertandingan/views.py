from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.db import connection

def get_semua_pertandingan(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT p.id_pertandingan, tp.nama_tim, p.start_datetime FROM PERTANDINGAN p JOIN TIM_PERTANDINGAN tp ON p.id_pertandingan=tp.id_pertandingan GROUP BY p.id_pertandingan, tp.nama_tim ORDER BY p.start_datetime ASC")
        data = cursor.fetchall()
    
    result = []

    for i in range(len(data)):
        result.append(
            data[i]
        )

    # print(result)

    return render(request, 'list_pertandingan.html', {'pertandingans': result})

def is_panitia(id):
    # Implementasikan logika untuk mengecek apakah user adalah panitia
    # Misalnya, Anda dapat menggunakan perintah request.user.groups.filter(name='panitia').exists()
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM PANITIA WHERE ID = %s", [id])
        data = cursor.fetchall()

    if data != None:
        return True
    else:
        return False

def get_avail_stadium(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT id_stadium, nama FROM STADIUM")
        data = cursor.fetchall()

    result = []

    for row in data:
        stadium_id, stadium_name = row
        result.append((stadium_id, stadium_name))

    # print(result)

    return render(request, 'pembuatan_pertandingan.html', {'stadiums': result})

def get_all_wasit(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, CONCAT(nama_depan, ' ', nama_belakang) FROM NON_PEMAIN WHERE id IN (SELECT id_wasit FROM WASIT)")
        data = cursor.fetchall()

    result = []

    for row in data:
        id_wasit, nama = row
        result.append((id_wasit, nama))

    print(result)

    return render(request, 'buat_pertandingan.html', {'wasits': result})

def delete_pertandingan(row_id):
    try:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM PERTANDINGAN WHERE id_pertandingan = %s", [row_id])
            cursor.execute("DELETE FROM TIM_PERTANDINGAN WHERE id_pertandingan = %s", [row_id])
            cursor.execute("DELETE FROM WASIT_PERTANDINGAN WHERE id_pertandingan = %s", [row_id])
            cursor.execute("DELETE FROM PEMAIN_PERTANDINGAN WHERE id_pertandingan = %s", [row_id])
    
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'failed'})
