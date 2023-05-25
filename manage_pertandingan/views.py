from django.shortcuts import render
from django.db import connection

def fetch(cursor):
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

def show_manage_pertandingan(request):
    query_jumlah_pertandingan = f"""
        SELECT COUNT(*) as jumlah_pertandingan
        FROM PERTANDINGAN;
        """
    cursor = connection.cursor()
    cursor.execute(query_jumlah_pertandingan)
    jumlah_pertandingan = fetch(cursor)

    query_pertandingan = f"""
        SELECT pertandingan.id_pertandingan, ARRAY_AGG(tim_pertandingan.nama_tim) as tim, start_datetime
        FROM pertandingan, tim_pertandingan
        WHERE pertandingan.id_pertandingan=tim_pertandingan.id_pertandingan
        GROUP BY pertandingan.id_pertandingan
        ORDER BY start_datetime;
        """
    cursor = connection.cursor()
    cursor.execute(query_pertandingan)
    pertandingan = fetch(cursor)
    
    # list_pertandingan = []
    # for data in pertandingan:
    #     data['dua_tim'] = data['nama_tim_1'] + "," + data['nama_tim_2']
    #     list_pertandingan.append(data)
    
    pemenang = {}
    for i in pertandingan:
        query_skor = f"""
            SELECT nama_tim, skor
            FROM TIM_PERTANDINGAN
            WHERE id_pertandingan = '{i['id_pertandingan']}';
            """
        cursor = connection.cursor()
        cursor.execute(query_skor)
        skor_pertandingan = fetch(cursor)

        if skor_pertandingan[0]['skor'] > skor_pertandingan[1]['skor']:
            pemenang[i['id_pertandingan']] = skor_pertandingan[0]['nama_tim']
        elif skor_pertandingan[1]['skor'] > skor_pertandingan[0]['skor']:
            pemenang[i['id_pertandingan']] = skor_pertandingan[1]['nama_tim']
        else:
            pemenang[i['id_pertandingan']] = "-"

    response = {
        'jumlah_pertandingan': jumlah_pertandingan[0]['jumlah_pertandingan'],
        'pertandingan': pertandingan,
        'pemenang' : pemenang
    }
    return render(request, 'manage_pertandingan.html', response)


# def show_manage_pertandingan_sebelum(request):
#     return render(request, 'manage_pertandingan_sebelum.html')

# def show_list_pertandingan_stage(request):
#     return render(request, 'list_pertandingan_stage.html')

# def show_list_pertandingan_nonstage(request):
#     return render(request, 'list_pertandingan_nonstage.html')

# def show_manage_pertandingan_sesudah(request):
#     return render(request, 'manage_pertandingan_sesudah.html')

def show_lihat_peristiwa(request, id_pertandingan, nama_tim):
    query_peristiwa = f"""
        SELECT *
        FROM PEMAIN AS pm
        JOIN PERISTIWA AS ps ON pm.id_pemain = ps.id_pemain
        WHERE pm.nama_tim = '{nama_tim}'
        AND ps.id_pertandingan = '{id_pertandingan}';
        """
    
    cursor = connection.cursor()
    cursor.execute(query_peristiwa)
    peristiwa_pertandingan = fetch(cursor)

    print("ini fetch gua")
    print(id_pertandingan)
    print(nama_tim)
    print(peristiwa_pertandingan)

    response = {
        'nama_tim' : nama_tim,
        'peristiwa_pertandingan' : peristiwa_pertandingan
    }

    return render(request, 'lihat_peristiwa.html', response)