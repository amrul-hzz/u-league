from django.shortcuts import render
from django.db import connection
from django.http import JsonResponse

def fetch(cursor):
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

def show_dashboard_penonton(request):
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
    # username_manajer = request.session("username")
    cursor.execute(f"""
    SELECT id_manajer
    FROM MANAJER
    WHERE username = 'vdeantoni15'
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

    nama_tim = str(cursor.fetchone()[0])
    print(nama_tim)

    cursor.execute(f"""
    SELECT *
    FROM PEMAIN
    WHERE nama_tim = '{nama_tim}'
    """)

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

    return render(request, 'dashboard_manajer.html', {
        "nama_depan": str(data_manajer[1]),
        "nama_belakang": str(data_manajer[2]),
        "no_hp": str(data_manajer[3]),
        "email": str(data_manajer[4]),
        "alamat": str(data_manajer[5]),
        "status": str(data_manajer[7]),
        "nama_tim": nama_tim,
        "pemain": pemain,
    })

def show_dashboard_panitia(request):
    cursor = connection.cursor()
    # username_panitia = request.session("username")
    cursor.execute(f"""
    SELECT id_panitia, jabatan
    FROM PANITIA
    WHERE username = 'jspackmank'
    """)

    data_panitia = cursor.fetchone()
    id_panitia = str(data_panitia[0])
    print(id_panitia)

    jabatan_panitia = str(data_panitia[1])
    print(jabatan_panitia)

    cursor.execute(f"""
    SELECT *
    FROM NON_PEMAIN
    JOIN STATUS_NON_PEMAIN ON id_non_pemain = id
    WHERE id_non_pemain = '{id_panitia}'
    """)

    data_final = cursor.fetchone()

    cursor.execute(f"""
    SELECT *
    FROM RAPAT
    WHERE perwakilan_panitia = '{id_panitia}'
    """)

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
        "nama_depan": data_final[1],
        "nama_belakang": data_final[2],
        "no_hp": data_final[3],
        "email": data_final[4],
        "alamat": data_final[5],
        "status": data_final[7],
        "jabatan": jabatan_panitia,
        "rapat": rapat,
    })
