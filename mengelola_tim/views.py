from django.shortcuts import render, redirect
from django.db import connection
from django.contrib import messages

# Create your views here.
def mengelola_tim(request):
    return render(request, "pendaftaran_tim.html")

def create_tim(request):
    cursor = connection.cursor()

    if request.method == "POST":
        nama_tim = request.POST.get("nama_tim")
        nama_universitas = request.POST.get("nama_universitas")
        # id_manajer = request.session("nama")
        try:
            cursor.execute(f"""
            INSERT INTO TIM VALUES ('{nama_tim}', '{nama_universitas}');

            INSERT INTO TIM_MANAJER VALUES ('18aa5c26-6c61-454e-afd3-346fe7be83f7', '{nama_tim}');
            
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
    WHERE username = 'cobalagi'
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
        # nama_tim = str(cursor.fetchone()[0])
        # print(nama_tim)

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

    # try:
    #     nama_univ = cursor.fetchone()[0]
    # except Exception as e:
    #     messages.error(request,e)

    # # 5. ambil nama2 pemain dari tabel pemain 
    # cursor.execute(f"""
    # SELECT *
    # FROM PEMAIN
    # WHERE nama_tim = '{nama_tim}'
    # ORDER BY id_pemain;
    # """)

    # data_pemain = cursor.fetchall()

    # pemain = []

    # if data_pemain:
    #     for i in data_pemain:
    #         pemain.append(
    #             {
    #                 "nama_pemain": i[2] + " " + i[3],
    #                 "no_hp": i[4],
    #                 "tanggal_lahir": i[5],
    #                 "is_captain": i[6],
    #                 "posisi": i[7],
    #                 "npm": i[8],
    #                 "jenjang": i[9],
    #                 "id_pemain": i[0],
    #             }
    #         )

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
    cursor = connection.cursor()
    cursor.execute(f"""
    UPDATE PEMAIN
    SET IS_CAPTAIN = TRUE
    WHERE id_pemain = '{id}';
    """)

    return redirect("/mengelolatim/")

def delete_pemain(request, id):
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
    cursor = connection.cursor()
    cursor.execute(f"""
    UPDATE PELATIH
    SET nama_tim = null
    WHERE id_pelatih = '{id}'
    """)

    return redirect("/mengelolatim")

def show_pemain_null(request):
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
    print("masuk sini")
    cursor = connection.cursor()
    if request.method == "POST":
        data_pemain = str(request.POST.get("dropdown")).split("-")
        nama_pemain = str(data_pemain[0]).split(" ")
        print(data_pemain)
        print(nama_pemain)
        nama_depan = nama_pemain[0]
        nama_belakang = nama_pemain[1]
        posisi = data_pemain[1]
        # nama_tim = request.session("nama_tim")
        print("nama depan: "+nama_depan)
        print("nama belakang: "+nama_belakang)
        print("posisi: "+posisi)

        cursor.execute(f"""
        SELECT id_pemain
        FROM PEMAIN
        WHERE nama_depan = '{nama_depan}' AND
            nama_belakang = '{nama_belakang}';
        """)

        id_pemain = str(cursor.fetchone()[0])
        print(id_pemain)

        try:
            cursor.execute(f"""
            UPDATE PEMAIN
            SET nama_tim = 'The Mavericks'
            WHERE id_pemain = '{id_pemain}';
            """)

            return redirect("/mengelolatim/")
        except Exception as e:
            messages.error(request,e)

    return render(request, "daftar_pemain.html")

def show_pelatih_null(request):
    print("masuk sini ga")
    cursor = connection.cursor()
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

def add_pelatih(request):
    cursor = connection.cursor()
    if request.method == "POST":
        data_pelatih = str(request.POST.get("dropdown")).split("-")
        nama_pelatih = str(data_pelatih[0]).split(" ")
        print(data_pelatih)
        print(nama_pelatih)
        nama_depan = nama_pelatih[0]
        nama_belakang = nama_pelatih[1]
        spesialisasi = data_pelatih[1]
        # nama_tim = request.session("nama_tim")
        print("nama depan: "+nama_depan)
        print("nama belakang: "+nama_belakang)
        print("spesialisasi: "+spesialisasi)

        cursor.execute(f"""
        SELECT id
        FROM NON_PEMAIN
        WHERE nama_depan = '{nama_depan}' AND
            nama_belakang = '{nama_belakang}';
        """)

        id_pelatih = str(cursor.fetchone()[0])
        print(id_pelatih)

        try:
            cursor.execute(f"""
            UPDATE PELATIH
            SET nama_tim = 'The Mavericks'
            WHERE id_pelatih = '{id_pelatih}';
            """)
            print("masuk sini")

            return redirect("/mengelolatim/")
        except Exception as e:
            print("masuk sini error")
            messages.error(request,e)

    return render(request, "daftar_pelatih.html")