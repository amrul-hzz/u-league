from django.shortcuts import render
from django.db import connection
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# def show_mulai_pertandingan(request, dua_tim):
#     print(dua_tim)
#     dua_tim = dua_tim.split(",")
#     response = {'nama_tim_1':dua_tim[0], 'nama_tim_2':dua_tim[1]}
#     return render(request, 'mulai_pertandingan.html', response)

# def show_pilih_peristiwa1(request, nama_tim):
#     print(nama_tim)
#     response = {}
#     response['nama_tim'] = nama_tim
#     return render(request, 'pilih_peristiwa1.html', response)

# def show_pilih_peristiwa2(request):
#     return render(request, 'pilih_peristiwa2.html')

def fetch(cursor):
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

def show_mulai_pertandingan(request, id_pertandingan):
    query = f"""
        SELECT ARRAY_AGG(nama_tim) as nama_tim, id_pertandingan
        FROM tim_pertandingan
        WHERE id_pertandingan='{id_pertandingan}'
        GROUP BY id_pertandingan;
        """
    cursor = connection.cursor()
    cursor.execute(query)
    data = fetch(cursor)

    response = {
        "data": data[0]
    }
    return render(request, 'mulai_pertandingan.html', response)

@csrf_exempt
def show_pilih_peristiwa(request, id_pertandingan, nama_tim):
    if request.method == "POST":
        pemain1 = request.POST.get('pemain1') 
        pemain2 = request.POST.get('pemain2') 
        peristiwa1 = request.POST.get('peristiwa1') 
        peristiwa2 = request.POST.get('peristiwa2') 
        waktu1 = request.POST.get('waktu1') 
        waktu1 = str(waktu1).replace("T", " ") + ":00"
        waktu2 = request.POST.get('waktu2') 
        waktu2 = str(waktu2).replace("T", " ") + ":00"
        peristiwa = [[pemain1, peristiwa1, waktu1], [pemain2, peristiwa2, waktu2]]

        for data in peristiwa:
            if data[0] == 0 or data[1] == 0 or len(data[2]) < 19:
                continue
            else:
                query = f"""
                    INSERT INTO peristiwa VALUES(
                    '{id_pertandingan}', '{data[2]}', '{data[1]}', '{data[0]}'
                    );
                    """
                cursor = connection.cursor()
                cursor.execute(query)
                insert_data = fetch(cursor)

        if type(insert_data) != int  :
            return JsonResponse({'success': 'false', 'message': 'Something is wrong'}, status = 200)
        else:
            return JsonResponse({'success': 'true', 'message': 'Berhasil menyimpan peristiwa.'}, status=200)        
    else:
        query = f"""
            SELECT pertandingan.id_pertandingan, tim_pertandingan.nama_tim, JSON_AGG(JSON_BUILD_ARRAY(id_pemain, pemain.nama_depan, pemain.nama_belakang)) as nama_pemain
            FROM pertandingan, tim_pertandingan, pemain
            WHERE pertandingan.id_pertandingan=tim_pertandingan.id_pertandingan
            AND tim_pertandingan.nama_tim=pemain.nama_tim
            AND pertandingan.id_pertandingan='{id_pertandingan}'
            AND tim_pertandingan.nama_tim='{nama_tim}'
            GROUP BY pertandingan.id_pertandingan, tim_pertandingan.nama_tim;
            """
        cursor = connection.cursor()
        cursor.execute(query)
        data = fetch(cursor)
        
        context = {
            'data': data[0]
        }
        return render(request, 'pilih_peristiwa.html',context)