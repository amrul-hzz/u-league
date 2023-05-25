from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.db import connection
import uuid
import json

def get_all_pertandingan(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT p.id_pertandingan, tp.nama_tim, p.start_datetime FROM PERTANDINGAN p JOIN TIM_PERTANDINGAN tp ON p.id_pertandingan=tp.id_pertandingan GROUP BY p.id_pertandingan, tp.nama_tim ORDER BY p.start_datetime ASC")
        data = cursor.fetchall()
    
    result = []

    for i in range(len(data)):
        result.append(
            data[i]
        )

    pertandingans_json = json.dumps([str(uuid) for uuid in result])

    context = {'pertandingans_json': pertandingans_json,
                'pertandingans': result}

    # print(result)

    return render(request, 'list_pertandingan.html', context)

def get_all_stadium(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT id_stadium, nama FROM STADIUM")
        data = cursor.fetchall()

    result = []

    for i in range(len(data)):
        result.append(
            data[i]
        )

    stadiums_json = json.dumps([str(uuid) for uuid in result])

    context = {'stadiums_json': stadiums_json,
                'stadiums': result}

    # print(result)

    return render(request, 'pembuatan_pertandingan.html', context)

def get_all_wasit_tim(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, CONCAT(nama_depan, ' ', nama_belakang) FROM NON_PEMAIN WHERE id IN (SELECT id_wasit FROM WASIT)")
        data_wasit = cursor.fetchall()

    result_wasit = []

    for i in range(len(data)):
        result_wasit.append(
            data_wasit[i]
        )

    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM TIM_PERTANDINGAN tp JOIN TIM t ON tp.nama_tim = t.nama_tim")
        data_tim = cursor.fetchall()

    result_tim = []

    for i in range(len(data)):
        result_tim.append(
            data_tim[i]
        )

    context = {'wasits': result_wasit,
                'tims': result_tim}

    # print(result)

    return render(request, 'buat_pertandingan.html', context)

def delete_pertandingan(request, row_id):
    print(row_id)
    if request.method == 'POST':
        try:
            with connection.cursor() as cursor:
                print(row_id)
                cursor.execute("DELETE FROM PERTANDINGAN WHERE id_pertandingan = %s", [row_id])
                cursor.execute("DELETE FROM TIM_PERTANDINGAN WHERE id_pertandingan = %s", [row_id])
                cursor.execute("DELETE FROM WASIT_PERTANDINGAN WHERE id_pertandingan = %s", [row_id])
                cursor.execute("DELETE FROM PEMAIN_PERTANDINGAN WHERE id_pertandingan = %s", [row_id])
        
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'failed'})

def create_pertandingan(request, row_id):
    with connection.cursor() as cursor:
        stadium = request.get['stadium-dropdown']
        wasit_utama = request.get['wasit_utama']
        wasit_pembantu1 = request.get['wasit_pendamping']
        wasit_pembantu2 = request.get['wasit_pendamping2']
        wasit_cadangan = request.get['wasit_cadangan']
        tim1 = request.get['tim1']
        tim2 = request.get['tim2']

        print(stadium, wasit_utama, wasit_pembantu1, wasit_pembantu2, wasit_cadangan, tim1, tim2)

        cursor.execute("UPDATE PERTANDINGAN SET id_stadium = %s WHERE id_pertandingan = %s", [request.POST['start_datetime'], request.POST['end_datetime'], request.POST['id_stadium'], row_id])
        
        return render(request, 'buat_pertandingan.html')

def select_pertandingan(request, row_id):
    context = {'row_id': row_id}
    return render(request, 'buat_pertandingan.html', context)