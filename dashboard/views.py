from django.shortcuts import render, redirect
from django.db import connection
from django.contrib import messages
from django.http import HttpResponse
from authentication.views import *

def fetch(cursor):
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

def show_dashboard_penonton(request):
    if is_penonton(request.session['username']) == False:
        return HttpResponse("bukan penonton")    
    response = {}
    query = f"""
    SELECT * FROM penonton
    JOIN non_pemain ON id_penonton = id
    WHERE id_penonton IN (
        SELECT id_penonton FROM penonton WHERE username = '{request.session['username']}'
    );"""

    cursor = connection.cursor()
    cursor.execute(query)
    user_data = fetch(cursor)

    for data in user_data:
        request.session['id'] = str(data['id'])
        response['nama_depan'] = data['nama_depan']
        response['nama_belakang'] = data['nama_belakang']
        response['nomor_hp'] = data['nomor_hp']
        response['email'] = data['email']
        response['alamat'] = data['alamat']

    query = f"""
    SELECT status FROM status_non_pemain
    WHERE id_non_pemain = '{request.session['id']}';"""
    cursor.execute(query)
    user_data = fetch(cursor)

    for data in user_data:
        response['status'] = data['status']

    return render(request, 'dashboard_penonton.html', response)

def show_dashboard(request):
    return render(request, "dashboard_manajer.html")

def show_dashboard_manajer(request):
    
    cursor = connection.cursor()
    username_manajer = request.session['username']
    if is_manajer(username_manajer) == False:
        return HttpResponse("bukan manajer")
    cursor.execute(f"""
    SELECT id_manajer
    FROM MANAJER
    WHERE username = '{username_manajer}'
    """)

    id_manajer = str(cursor.fetchone()[0])

    cursor.execute(f"""
    SELECT *
    FROM NON_PEMAIN
    JOIN STATUS_NON_PEMAIN ON id = id_non_pemain
    WHERE id = '{id_manajer}'
    """)

    data_manajer = cursor.fetchone()

    cursor.execute(f"""
    SELECT nama_tim
    FROM TIM_MANAJER
    WHERE id_manajer = '{id_manajer}'
    """)

    nama_tim = None

    try:
        nama_tim = str(cursor.fetchone()[0])

        cursor.execute(f"""
        SELECT *
        FROM PEMAIN
        WHERE nama_tim = '{nama_tim}'
        """)

    except Exception as e:
        messages.error(request,e)

    nama_univ = None
    
    try:
        cursor.execute(f"""
        SELECT universitas
        FROM TIM
        WHERE nama_tim = '{nama_tim}'
        """)
        nama_univ = cursor.fetchone()[0]
    except Exception as e:
        messages.error(request,e)
        
    data_pemain = cursor.fetchall()
    pemain = []

    indexing = 1

    if data_pemain:
        for i in data_pemain:
            pemain.append(
                {
                    "nama_pemain": i[2] + " " + i[3],
                    "indeks": indexing,
                }
            )
            indexing += 1
    
    data_tim = []

    if nama_tim:
        data_tim.append(
            {
                "nama_tim":nama_tim,
                "nama_univ": nama_univ,
                "pemain":pemain
            }
        )

    print("$$$$$$$$", data_manajer)

    return render(request, 'dashboard_manajer.html', {
        "nama_depan": str(data_manajer[1]),
        "nama_belakang": str(data_manajer[2]),
        "no_hp": str(data_manajer[3]),
        "email": str(data_manajer[4]),
        "alamat": str(data_manajer[5]),
        "status": str(data_manajer[7]),
        "data_tim":data_tim
    })

def show_dashboard_panitia(request):    
    cursor = connection.cursor()
    username_panitia = request.session['username']
    if is_panitia(username_panitia) == False:
        return HttpResponse("bukan panitia")
        
    cursor.execute(f"""
    SELECT id_panitia, jabatan
    FROM PANITIA
    WHERE username = '{username_panitia}'
    """)

    data_panitia = cursor.fetchone()
    id_panitia = str(data_panitia[0])

    jabatan_panitia = str(data_panitia[1])

    nama_depan = None
    nama_belakang = None
    no_hp = None
    email = None
    alamat = None
    status = None

    try:
        cursor.execute(f"""
        SELECT *
        FROM NON_PEMAIN
        JOIN STATUS_NON_PEMAIN ON id_non_pemain = id
        WHERE id_non_pemain = '{id_panitia}'
        """)

        print("id panitia final:" + id_panitia)
        data_final = cursor.fetchone()

        print("masuk gasih")

        print(data_final)

        nama_depan = data_final[1]
        nama_belakang = data_final[2]
        no_hp = data_final[3]
        email = data_final[4]
        alamat = data_final[5]
        status = data_final[7]
    except Exception as e:
        messages.error(request,e)

    data_rapat = None

    try:
        cursor.execute(f"""
        SELECT *
        FROM RAPAT
        WHERE perwakilan_panitia = '{id_panitia}'
        """)
    except Exception as e:
        messages.error(request,e)

    data_rapat = cursor.fetchall()

    rapat = []

    if data_rapat:
        for i in data_rapat:
            rapat.append(
                {
                    "id_pertandingan": i[0],
                    "datetime": i[1],
                }
            )
   
    return render(request, 'dashboard_panitia.html', {
        "nama_depan": nama_depan,
        "nama_belakang": nama_belakang,
        "no_hp": no_hp,
        "email": email,
        "alamat": alamat,
        "status": status,
        "jabatan": jabatan_panitia,
        "rapat": rapat,
    })