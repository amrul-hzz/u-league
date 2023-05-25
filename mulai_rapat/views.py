from django.shortcuts import redirect, render
from django.db import connection
from django.http import HttpResponseRedirect
from django.contrib import messages

def mulai_rapat(request):
    cursor = connection.cursor()

    # get daftar pertandingan
    cursor.execute(f'''
        SELECT * FROM PERTANDINGAN;
    ''')
    pertandingan = cursor.fetchall()

    # get nama tim, waktu, stadium
    pertandingan_list = []
    for p in pertandingan:
        # get nama tim
        cursor.execute(f'''
            select * from TIM_PERTANDINGAN where id_pertandingan = '{p[0]}';
        ''')
        tim = cursor.fetchall()

        # get stadium
        cursor.execute(f'''
            select nama from PERTANDINGAN JOIN STADIUM ON stadium = id_stadium 
            where stadium = '{p[3]}';
        ''')
        stadium = cursor.fetchall()

        # cek apakah sudah ada rapat atau belum
        cursor.execute(f'''
            select id_pertandingan from RAPAT where id_pertandingan = '{p[0]}';
        ''')
        rapat = cursor.fetchall()
        bool_rapat = False
        if len(rapat) > 0: bool_rapat = True

        # jadikan dalam bentuk dict
        pertandingan_list.append({
            "tim1": tim[0][0],
            "tim2": tim[1][0],
            "waktu": p[1].strftime("%d %B %Y %H:%M") + " - " + p[2].strftime("%H:%M"),
            "stadium": stadium[0][0],
            "rapat": bool_rapat,
            "id_pertandingan": p[0]
        })
        
    return render(request, "pilih_pertandingan.html", {"pertandingan_list": pertandingan_list})

def rapat_pertandingan(request, tim1, tim2):
    cursor = connection.cursor()
    if request.method == 'POST':

        username_panitia = request.session.get('username')

        # get id pertandingan
        cursor.execute(f'''
            SELECT A.id_pertandingan 
            FROM TIM_PERTANDINGAN A, TIM_PERTANDINGAN B
            WHERE a.nama_tim = '{tim1}' AND b.nama_tim = '{tim2}' 
            AND A.id_pertandingan = B.id_pertandingan;
        ''')
        id_pertandingan = cursor.fetchall()

        #get id panitia
        cursor.execute(f'''
            SELECT id_panitia
            FROM panitia
            WHERE username = '{username_panitia}'
        ''')
        id_panitia = cursor.fetchall()

        #get id_manajer tim a
        cursor.execute(f'''
            SELECT id_manajer
            FROM tim_manajer
            WHERE nama_tim = '{tim1}'
        ''')
        id_manajer_a = cursor.fetchall()

        #get id_manajer tim b
        cursor.execute(f'''
            SELECT id_manajer
            FROM tim_manajer
            WHERE nama_tim = '{tim2}'
        ''')
        id_manajer_b = cursor.fetchall()

        #get waktu rapat
        cursor.execute(f''' select current_timestamp;''')
        waktu_rapat = cursor.fetchall()

        #get isi rapat
        isi_rapat = request.POST.get('isi_rapat')
        print(isi_rapat)

        try:
            #insert rapat
            cursor.execute(f''' insert into rapat values ('{id_pertandingan[0][0]}', '{waktu_rapat[0][0]}', 
            '{id_panitia[0][0]}', '{id_manajer_a[0][0]}', '{id_manajer_b[0][0]}', '{isi_rapat}');''')
            print("insert rapat berhasil")
            return redirect('/mulairapat/')
        except Exception as e:
            messages.error(request, e)
            print(e)
    
    cursor.close()
    return render(request, "rapat_pertandingan.html",{
        'tim1' : tim1,
        'tim2' : tim2
    })
