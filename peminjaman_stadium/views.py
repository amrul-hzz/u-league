from django.shortcuts import render
from django.db import connection
from authentication.views import *

# Create your views here.
def list_pemesanan(request):
    cursor = connection.cursor()
    cursor.execute(f''' 
        select s.nama, p.start_datetime, p.end_datetime
        from stadium s, peminjaman p
        where s.id_stadium = p.id_stadium
        order by p.start_datetime desc;
    ''')
    pemesanan = cursor.fetchall()

    pemesanan_list = []
    for stadium in pemesanan:
        pemesanan_list.append({
            "nama_stadium": stadium[0],
            "start_datetime": stadium[1],
            "end_datetime": stadium[2]
        })
    connection.close()

    context = {'pemesanan_list': pemesanan_list}
    return render(request, "list_pemesanan.html", context)

def pilih_stadium(request):
    cursor = connection.cursor()
    cursor.execute(f'''
        select nama, id_stadium
        from stadium;
    ''')
    stadium = cursor.fetchall()
    connection.close()

    stadium_list = []
    for s in stadium:
        stadium_list.append({
            "nama_stadium": s[0],
            "id_stadium": s[1]
        })
    
    context = {'stadium_list': stadium_list}
    return render(request, "pilih_stadium.html", context)

def add_pemesanan(request):
    if request.method == "POST":
        tanggal = request.POST.get("date")
        id_stadium = request.POST.get("id_stadium")
        username = request.session['username']
        cursor = connection.cursor()

        cursor.execute(
            f"""
            SELECT id_manajer
            FROM manajer
            WHERE username = '{username}'
            """
        )
        id_manajer = cursor.fetchone()[0]

        try:
            cursor.execute(f"""
            INSERT INTO PEMINJAMAN (id_manajer, start_datetime, end_datetime, id_stadium)
            VALUES ('{id_manajer}', '{tanggal}', '{tanggal}', '{id_stadium}');
            """)
            return redirect("/peminjaman_stadium/")
        except Exception as e:
            messages.error(request, e)
    
    # Handle request method other than POST
    # return render(request, "nama_template.html")

    
# def list_waktu(request):
#     date = request.POST.get('date')
#     id_stadium = request.POST.get('id_stadium')

#     #debug console
#     print(date)
#     print(id_stadium)

#     cursor = connection.cursor()
#     cursor.execute(f'''
#         select nama
#         from stadium
#         where id_stadium = '{id_stadium}'
#     ''')
#     nama_stadium = cursor.fetchmany(1)[0][0]
#     connection.close()
#     context = {
#         'nama_stadium': nama_stadium,
#         'date': date,
#     }

#     return render(request, "list_waktu.html", context)

# # fungsi untuk mengupdate list pemesanan di list_pemesanan.html
# def update_list_pemesanan(request):
#     cursor = connection.cursor()
#     cursor.execute(f''' 
#         select s.nama, p.start_datetime, p.end_datetime
#         from stadium s, peminjaman p
#         where s.id_stadium = p.id_stadium;
#     ''')
#     pemesanan = cursor.fetchall()

#     pemesanan_list = []
#     for stadium in pemesanan:
#         pemesanan_list.append({
#             "nama_stadium": stadium[0],
#             "start_datetime": stadium[1],
#             "end_datetime": stadium[2]
#         })
#     connection.close()

#     context = {'pemesanan_list': pemesanan_list}
#     return render(request, "update_list_pemesanan.html", context)
