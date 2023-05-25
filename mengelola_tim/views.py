from django.shortcuts import render, redirect
from django.db import connection
from django.contrib import messages
from django.http import HttpResponse
from authentication.views import *

# Create your views here.
def mengelola_tim(request):
    if is_manajer(request.session['username']) == False:
        return HttpResponse("bukan manajer")
    return render(request, "pendaftaran_tim.html")

def create_tim(request):
    if is_manajer(request.session['username']) == False:
        return HttpResponse("bukan manajer")
    cursor = connection.cursor()

    if request.method == "POST":
        nama_tim = request.POST.get("nama_tim")
        nama_universitas = request.POST.get("nama_universitas")
        id_manajer = request.session['username']
        try:
            cursor.execute(f"""
            INSERT INTO TIM VALUES ('{nama_tim}', '{nama_universitas}');

            INSERT INTO TIM_MANAJER VALUES ('{id_manajer}', '{nama_tim}');
            
            """)

            return redirect("/dashboard/dashboard_manajer/")
        except Exception as e:
            messages.error(request,e)

    return render(request, "pendaftaran_tim.html")

def get_tim(request):
    if is_manajer(request.session['username']) == False:
        return HttpResponse("bukan manajer")
    cursor = connection.cursor()
    # 1. get username si manajer
    nama_manajer = request.session['username']
    # 2. ambil id dr tabel manajer
    cursor.execute(f"""
    SELECT *
    FROM MANAJER
    WHERE username = '{nama_manajer}'
    """)
    # WHERE username = 'vdeantoni15'

    try:
        id_manajer = str(cursor.fetchone()[0])
    except Exception as e:
        messages.error(request,e)

    # 3. ambil nama tim si id manajer itu di tim_manajer
    cursor.execute(f"""
    SELECT nama_tim
    FROM TIM_MANAJER
    WHERE id_manajer = '{id_manajer}'
    """)

    nama_tim = None

    try:
        nama_tim = cursor.fetchone()[0]
    except Exception as e:
        messages.error(request,e)

    # 4. ambil nama tim dan asal univ   

    try:
        cursor.execute(f"""
        SELECT *
        FROM PEMAIN
        WHERE nama_tim = '{nama_tim}'
        """)

    except Exception as e:
        messages.error(request,e)
    data_pemain = cursor.fetchall()

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

    pemain = []

    if data_pemain:
        for i in data_pemain:
            pemain.append(
                {
                    "nama_pemain": i[2] + " " + i[3],
                    "no_hp": i[4],
                    "tanggal_lahir": i[5],
                    "is_captain": i[6],
                    "posisi": i[7],
                    "npm": i[8],
                    "jenjang": i[9],
                    "id_pemain": i[0],
                }
            )
    
    data_tim = []

    if nama_tim:
        data_tim.append(
            {
                "nama_tim":nama_tim,
                "pemain":pemain
            }
        )

    # 6. ambil nama2 pelatih dari tabel pelatih
    cursor.execute(f"""
    SELECT id_pelatih
    FROM PELATIH
    WHERE nama_tim = '{nama_tim}'
    ORDER BY id_pelatih;
    """)

    data_pelatih = cursor.fetchall()

    pelatih = []

    for i in data_pelatih:
        cursor.execute(f"""
        SELECT *
        FROM NON_PEMAIN
        JOIN SPESIALISASI_PELATIH ON non_pemain.id = spesialisasi_pelatih.id_pelatih
        WHERE id = '{i[0]}'
        """)

        result = cursor.fetchone()

        pelatih.append(
            {
                "nama_pelatih": result[1] + " " + result[2],
                "no_hp": result[3],
                "email": result[4],
                "alamat": result[5],
                "spesialisasi": result[7],
                "id_pelatih": result[0],
            }
        )

    return render(request, "tim.html", {
        "nama_tim": nama_tim,
        "nama_univ": nama_univ,
        "data_tim": data_tim,
        "pelatih": pelatih,
    }) 

def make_captain(request, id):
    if is_manajer(request.session['username']) == False:
        return HttpResponse("bukan manajer")
    cursor = connection.cursor()
    cursor.execute(f"""
    UPDATE PEMAIN
    SET IS_CAPTAIN = TRUE
    WHERE id_pemain = '{id}';
    """)

    return redirect("/mengelolatim/")

def delete_pemain(request, id):
    if is_manajer(request.session['username']) == False:
        return HttpResponse("bukan manajer")
    cursor = connection.cursor()
    cursor.execute(f"""
    UPDATE PEMAIN
    SET nama_tim = null
    WHERE id_pemain = '{id}';

    UPDATE PEMAIN
    SET is_captain = false
    WHERE id_pemain = '{id}';
    """)

    return redirect("/mengelolatim")

def delete_pelatih(request, id):
    if is_manajer(request.session['username']) == False:
        return HttpResponse("bukan manajer")
    cursor = connection.cursor()
    cursor.execute(f"""
    UPDATE PELATIH
    SET nama_tim = null
    WHERE id_pelatih = '{id}'
    """)

    return redirect("/mengelolatim")

def show_pemain_null(request):
    if is_manajer(request.session['username']) == False:
        return HttpResponse("bukan manajer")
    cursor = connection.cursor()
    cursor.execute(f"""
    SELECT *
    FROM PEMAIN
    WHERE nama_tim IS NULL
    ORDER BY id_pemain;
    """)

    data_pemain = cursor.fetchall()

    pemain = []

    if data_pemain:
        for i in data_pemain:
            pemain.append(
                {
                    "nama_pemain": i[2] + " " + i[3],
                    "no_hp": i[4],
                    "tanggal_lahir": i[5],
                    "is_captain": i[6],
                    "posisi": i[7],
                    "npm": i[8],
                    "jenjang": i[9],
                    "id_pemain": i[0],
                }
            )

    return render(request, "daftar_pemain.html", {
        "pemain": pemain,
    })

def add_pemain(request):
    if is_manajer(request.session['username']) == False:
        return HttpResponse("bukan manajer")
    cursor = connection.cursor()
    
    if request.method == "POST":
        data_pemain = str(request.POST.get("dropdown")).split("-")

        if not data_pemain or len(data_pemain) < 2:
            return HttpResponse("Tidak ada pemain yang dapat ditambahkan")
        
        nama_pemain = str(data_pemain[0]).split(" ")
        nama_depan = nama_pemain[0]
        nama_belakang = nama_pemain[1]
        posisi = data_pemain[1]

        cursor.execute(f"""
        SELECT id_pemain
        FROM PEMAIN
        WHERE nama_depan = '{nama_depan}' AND
            nama_belakang = '{nama_belakang}';
        """)

        id_pemain = str(cursor.fetchone()[0])

        try:
            cursor.execute(f"""
            SELECT id_manajer
            FROM MANAJER
            WHERE username = '{request.session['username']}'
            """)

            id_manajer = str(cursor.fetchone()[0])

            cursor.execute(f"""
            SELECT nama_tim
            FROM TIM_MANAJER
            WHERE id_manajer = '{id_manajer}'
            """)

            nama_tim = str(cursor.fetchone()[0])

            cursor.execute(f"""
            UPDATE PEMAIN
            SET nama_tim = '{nama_tim}'
            WHERE id_pemain = '{id_pemain}';
            """)

            return redirect("/mengelolatim/")
        except Exception as e:
            messages.error(request,e)

    return render(request, "daftar_pemain.html")

def show_pelatih_null(request):
    if is_manajer(request.session['username']) == False:
        return HttpResponse("bukan manajer")
    cursor = connection.cursor()
    if request.method == "POST":
        id_pelatih = request.POST.get("id_pelatih")

        if not id_pelatih:
            return HttpResponse("Tidak ada pelatih yang dapat ditambahkan")

        cursor.execute(f"""
        SELECT id_manajer
        FROM MANAJER
        WHERE username = '{request.session['username']}'
        """)

        id_manajer = str(cursor.fetchone()[0])

        cursor.execute(f"""
        SELECT nama_tim
        FROM TIM_MANAJER
        WHERE id_manajer = '{id_manajer}'
        """)

        nama_tim = str(cursor.fetchone()[0])
        try:

            cursor.execute(f"""
            UPDATE PELATIH
            SET nama_tim = '{nama_tim}'
            WHERE id_pelatih = '{id_pelatih}';
            """)

            return redirect("/mengelolatim/")
        except Exception as e:
            messages.error(request,e)
    cursor.execute(f"""
    SELECT *
    FROM PELATIH
    WHERE nama_tim IS NULL
    ORDER BY id_pelatih;
    """)

    data_pelatih = cursor.fetchall()

    pelatih = []

    for i in data_pelatih:
        cursor.execute(f"""
        SELECT *
        FROM NON_PEMAIN
        JOIN SPESIALISASI_PELATIH ON non_pemain.id = spesialisasi_pelatih.id_pelatih
        WHERE id = '{i[0]}'
        """)

        result = cursor.fetchone()

        pelatih.append(
            {
                "nama_pelatih": result[1] + " " + result[2],
                "no_hp": result[3],
                "email": result[4],
                "alamat": result[5],
                "spesialisasi": result[7],
                "id_pelatih": result[0],
            }
        )

    return render(request, "daftar_pelatih.html", {
        "pelatih": pelatih,
    })