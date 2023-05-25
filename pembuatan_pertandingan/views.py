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

def get_all_wasit_tim(request, row_id):

    with connection.cursor() as cursor:
        cursor.execute("SELECT id, CONCAT(nama_depan, ' ', nama_belakang) FROM NON_PEMAIN WHERE id IN (SELECT id_wasit FROM WASIT)")
        data_wasit = cursor.fetchall()

    result_wasit = []

    for i in range(len(data_wasit)):
        result_wasit.append(
            data_wasit[i]
        )

    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM TIM_PERTANDINGAN tp JOIN TIM t ON tp.nama_tim = t.nama_tim")
        data_tim = cursor.fetchall()

    result_tim = []

    for i in range(len(data_tim)):
        result_tim.append(
            data_tim[i]
        )

    with connection.cursor() as cursor:
        cursor.execute("SELECT id_stadium, nama FROM STADIUM")
        data_stadium = cursor.fetchall()

    result_stadium = []

    for i in range(len(data_stadium)):
        result_stadium.append(
            data_stadium[i]
        )

    selected = []

    with connection.cursor() as cursor:
        cursor.execute("SELECT stadium FROM PERTANDINGAN WHERE id_pertandingan = %s", [row_id])
        selected_stadium = cursor.fetchall()
        selected.append(selected_stadium)

    with connection.cursor() as cursor:
        cursor.execute("SELECT id_wasit FROM WASIT_BERTUGAS WHERE id_pertandingan = %s AND posisi_wasit='Utama' ", [row_id])
        selected_wasit_utama = cursor.fetchall()
        selected.append(selected_wasit_utama)

    with connection.cursor() as cursor:
        cursor.execute("SELECT id_wasit FROM WASIT_BERTUGAS WHERE id_pertandingan = %s AND posisi_wasit='Hakim Garis' ", [row_id])
        selected_wasit_pembantu = cursor.fetchall()
        selected.append(selected_wasit_pembantu)

    with connection.cursor() as cursor:
        cursor.execute("SELECT nama_tim FROM TIM_PERTANDINGAN WHERE id_pertandingan = %s", [row_id])
        selected_tim = cursor.fetchall()
        selected.append(selected_tim)

    print(selected)

    context = {'wasits': result_wasit,
                'tims': result_tim,
                'stadiums': result_stadium,
                'selected': selected}

    return render(request, 'buat_pertandingan.html', context)

def delete_pertandingan(request, row_id):
    print(row_id)
    with connection.cursor() as cursor:
        print(row_id)
        cursor.execute("DELETE FROM PERTANDINGAN WHERE id_pertandingan = %s", [row_id])
        cursor.execute("DELETE FROM TIM_PERTANDINGAN WHERE id_pertandingan = %s", [row_id])
        cursor.execute("DELETE FROM WASIT_BERTUGAS WHERE id_pertandingan = %s", [row_id])

        return redirect ('/pembuatan_pertandingan')
        

def create_pertandingan(request, row_id):
    print(request.POST)
    with connection.cursor() as cursor:
        # stadium = request.POST.get('id-stadium')
        # wasit_utama = request.POST.get('wasit-utama')
        # wasit_pembantu1 = request.POST.get('wasit-pembantu1')
        # wasit_pembantu2 = request.POST.get('wasit-pembantu2')
        # wasit_cadangan = request.POST.get('wasit-cadangan')
        # tim1 = request.POST.get('tim1')
        # tim2 = request.POST.get('tim2')

        stadium = request.POST['id-stadium']
        wasit_utama = request.POST['wasit-utama']
        wasit_pembantu1 = request.POST['wasit-pembantu1']
        wasit_pembantu2 = request.POST['wasit-pembantu2']
        wasit_cadangan = request.POST['wasit-cadangan']
        tim1 = request.POST['tim1']
        tim2 = request.POST['tim2']
        
        print (stadium, wasit_utama, wasit_pembantu1, wasit_pembantu2, wasit_cadangan, tim1, tim2)

        cursor.execute("UPDATE PERTANDINGAN SET id_stadium = %s WHERE id_pertandingan = %s", [request.POST['id-stadium'], row_id])
        
        return redirect ('/pembuatan_pertandingan')