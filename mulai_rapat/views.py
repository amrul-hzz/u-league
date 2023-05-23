from django.shortcuts import render
from django.shortcuts import render
from django.db import connection
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.db import connection

def pilih_pertandingan(request):
    cursor = connection.cursor()
    cursor.execute(f'''
       SELECT
            CONCAT(tp1.Nama_Tim, ' vs ', tp2.Nama_Tim) AS "Tim Bertanding",
            s.Nama AS "Stadium",
            p.Start_DateTime || ' - ' || p.End_DateTime AS "Tanggal dan Waktu"
        FROM
            TIM_PERTANDINGAN tp1
            INNER JOIN TIM_PERTANDINGAN tp2 ON tp1.ID_Pertandingan = tp2.ID_Pertandingan
            INNER JOIN PERTANDINGAN p ON tp1.ID_Pertandingan = p.ID_Pertandingan
            INNER JOIN STADIUM s ON p.Stadium = s.ID_Stadium
        WHERE
            tp1.Nama_Tim < tp2.Nama_Tim;
    ''') # '<' to ensure theres only 1 row for each match
    pertandingan = cursor.fetchall()
    cursor.close()
    # print(pertandingan)

    cursor = connection.cursor()
    cursor.execute(f'''
        SELECT
            p.ID_Pertandingan,
            tma.ID_Manajer AS id_manajer_tim_a,
            tmb.ID_Manajer AS id_manajer_tim_b
        FROM
            PERTANDINGAN p
        JOIN TIM_PERTANDINGAN tpa ON p.ID_Pertandingan = tpa.ID_Pertandingan
        JOIN TIM_MANAJER tma ON tpa.Nama_Tim = tma.Nama_Tim
        JOIN TIM_PERTANDINGAN tpb ON p.ID_Pertandingan = tpb.ID_Pertandingan
        JOIN TIM_MANAJER tmb ON tpb.Nama_Tim = tmb.Nama_Tim
        WHERE
            tma.ID_Manajer > tmb.ID_Manajer;
    ''')
    rapat_util = cursor.fetchall()
    cursor.close()
    # print(rapat_util)
    pertandingan_list = []
    for i in range(len(pertandingan)):
        pertandingan_list.append({
            "tim_bertanding": pertandingan[i][0],
            "stadium": pertandingan[i][1],
            "tanggal_dan_waktu": pertandingan[i][2],


            "id_pertandingan": str(rapat_util[i][0]),
            "id_manajer_tim_a": str(rapat_util[i][1]),
            "id_manajer_tim_b": str(rapat_util[i][2])
        })

    context = {'pertandingan_list': pertandingan_list}
    return render(request, "pilih_pertandingan.html", context)

def rapat_pertandingan(request, pertandingan):
    # nama_tim = pertandingan.split(" vs ")

    # convert string to dict
    dict_pertandingan = eval(pertandingan)
    context = {
        'nama_tim': dict_pertandingan['tim_bertanding'],
        'pertandingan': pertandingan
        }
    print(pertandingan)
    
    return render(request, "rapat_pertandingan.html", context)

def create_rapat(request, pertandingan):
    isi_rapat = request.POST.get('isi_rapat')
    #debug console isi_rapat
    # print(isi_rapat)

    # convert string to dict
    dict_data = eval(pertandingan)

    cursor = connection.cursor()
    # error karena blm urus cookiesnya
    username = request.COOKIES['username']
    cursor.execute(f'''
        SELECT id_panitia
        FROM panitia
        WHERE username = '{username}'
    ''')
    id_panitia = cursor.fetchone()[0]

    cursor.execute(f'''
        INSERT INTO RAPAT (id_pertandingan, perwakilan_panitia, manajer_tim_a, manajer_tim_b, isi_rapat)
        VALUES ('{dict_data['id_pertandingan']}', '{id_panitia}', '{dict_data['id_manajer_tim_a']}', '{dict_data['id_manajer_tim_b']}', '{isi_rapat}')
    ''')
    
    return HttpResponseRedirect('/mulai_rapat/')
    #kalo dashboard panitia udah selesai return yang ini 
    # return HttpResponseRedirect('/dashboard/')
