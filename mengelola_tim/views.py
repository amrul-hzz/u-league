from django.shortcuts import render, redirect
from django.db import connection
from django.contrib import messages

# Create your views here.
def mengelola_tim(request):
    return render(request, "pendaftaran_tim.html")

def tim(request):
    return render(request, "tim.html")

def daftar_pemain(request):
    return render(request, "daftar_pemain.html")

def daftar_pelatih(request):
    return render(request, "daftar_pelatih.html")

def create_tim(request):
    cursor = connection.cursor()

    if request.method == "POST":
        nama_tim = request.POST.get("nama_tim")
        nama_universitas = request.POST.get("nama_universitas")
        # id_manajer = request.session("nama")
        try:
            cursor.execute(f"""
            INSERT INTO TIM VALUES ('{nama_tim}', '{nama_universitas}');

            INSERT INTO TIM_MANAJER VALUES ('3515bcb2-3a1b-4c97-ada4-f85f80486a30', '{nama_tim}');
            
            """)

            return redirect("/dashboard/dashboard_manajer/")
        except Exception as e:
            messages.error(request,e)

    return render(request, "pendaftaran_tim.html")

def get_tim(request):
    cursor = connection.cursor()
    # 1. get username si manajer
    # nama_manajer = request.session("username")
    # 2. ambil id dr tabel manajer
    cursor.execute(f"""
    SELECT *
    FROM MANAJER
    WHERE username = 'vdeantoni15'
    """)

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

    try:
        nama_tim = cursor.fetchone()[0]
    except Exception as e:
        messages.error(request,e)

    # 4. ambil nama tim dan asal univ
    cursor.execute(f"""
    SELECT universitas
    FROM TIM
    WHERE nama_tim = '{nama_tim}'
    """)

    try:
        nama_univ = cursor.fetchone()[0]
    except Exception as e:
        messages.error(request,e)

    # 5. ambil nama2 pemain dari tabel pemain 
    cursor.execute(f"""
    SELECT *
    FROM PEMAIN
    WHERE nama_tim = '{nama_tim}'
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
                }
            )

    # 6. ambil nama2 pelatih dari tabel pelatih
    cursor.execute(f"""
    SELECT id_pelatih
    FROM PELATIH
    WHERE nama_tim = '{nama_tim}'
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
            }
        )

    return render(request, "tim.html", {
        "nama_tim": nama_tim,
        "nama_univ": nama_univ,
        "pemain": pemain,
        "pelatih": pelatih,
    }) 

# def make_captain(request):
#     ConnectionRefusedError

# def delete_pemain(request)