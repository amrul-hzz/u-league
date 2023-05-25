from django.shortcuts import render, redirect
from django.db import connection
from django.contrib import messages
from django.http import HttpResponse
from authentication.views import *

def pilih_stadium(request):
    if is_penonton(request.session['username']) == False:
        return HttpResponse('bukan penonton')
    
    # get stadium id
    cursor = connection.cursor()
    cursor.execute(f"""
    SELECT ID_Stadium FROM STADIUM;
    """)
    stadium_id = cursor.fetchall()
    stadium_id = [str(x[0]) for x in stadium_id]

    # get stadium name
    stadium_name = []
    for id in stadium_id:
        cursor = connection.cursor()
        cursor.execute(f"""
        SELECT Nama FROM STADIUM
        WHERE ID_Stadium = '{id}';
        """)
        stadium_name.append(cursor.fetchone()[0])
    
    stadium_list = []
    for i in range(0, len(stadium_id)):
        stadium_list.append([stadium_id[i], stadium_name[i]])
    
    context = {
        'stadium_list': stadium_list,
    }

    return render(request, "pilih_stadium_tiket.html", context)

def list_waktu_dan_pertandingan(request):
    if is_penonton(request.session['username']) == False:
        return HttpResponse('bukan penonton')
    
    if request.method == "POST":
        stadium_id = request.POST.get("stadium")
        date = request.POST.get("date")

        # get stadium name
        cursor = connection.cursor()
        cursor.execute(f"""
        SELECT Nama FROM STADIUM 
        WHERE ID_stadium = '{stadium_id}';
        """)
        stadium_name = cursor.fetchone()[0]

        # get id pertandingan to get start, end, and teams
        cursor = connection.cursor()
        cursor.execute(f"""
        SELECT ID_Pertandingan FROM PERTANDINGAN
        WHERE ('{date}' BETWEEN DATE(Start_datetime) AND DATE(End_datetime));
        """)
        id_pertandingan = cursor.fetchall()
        id_pertandingan = [str(x[0]) for x in id_pertandingan]

        # get start time
        start = []
        for id in id_pertandingan:
            cursor = connection.cursor()
            cursor.execute(f"""
            SELECT Start_datetime FROM PERTANDINGAN
            WHERE ID_Pertandingan = '{id}';
            """)
            start.append(cursor.fetchone()[0])

        # get end time
        end = []
        for id in id_pertandingan:
            cursor = connection.cursor()
            cursor.execute(f"""
            SELECT End_datetime FROM PERTANDINGAN
            WHERE ID_Pertandingan = '{id}';
            """)
            end.append(cursor.fetchone()[0])
        
        # get playing teams
        team1 = []
        team2 = []
        for id in id_pertandingan:
            cursor = connection.cursor()
            cursor.execute(f"""
            SELECT Nama_Tim
            FROM TIM_PERTANDINGAN
            WHERE ID_Pertandingan = '{id}';
            """)
            team1.append(cursor.fetchone()[0])
            team2.append(cursor.fetchone()[0])

        # combine data
        match_list = []
        for i in range (0, len(id_pertandingan)):
            match = [id_pertandingan[i], start[i], end[i], team1[i], team2[i]]
            match_list.append(match)
      
        context = {
            "stadium_name": stadium_name,
            "match_list": match_list
        }

        return render(request, 'list_waktu_dan_pertandingan.html', context)
     
def beli_tiket(request, id_pertandingan):
    if is_penonton(request.session['username']) == False:
        return HttpResponse('bukan penonton')

    context = {
        "id_pertandingan": id_pertandingan,
    }
     
    return render(request, "beli_tiket.html", context)

def create_pembelian_tiket(request, id_pertandingan):
    if is_penonton(request.session['username']) == False:
        return HttpResponse('bukan penonton')
    
    if request.method == 'POST':

        # generate nomor receipt 
        cursor = connection.cursor()
        cursor.execute(f"""
        SELECT COUNT(*) FROM PEMBELIAN_TIKET;
        """)
        ticket_cnt = cursor.fetchone()[0]

        if (len(str(ticket_cnt)) > 49):
            return HttpResponse('tiket habis')
        
        nomor_receipt = 'R' + str(ticket_cnt + 1)

        # get id_penonton
        cursor = connection.cursor()
        cursor.execute(f"""
        SELECT ID_Penonton FROM PENONTON
        WHERE Username = '{request.session['username']}';
        """)
        id_penonton = cursor.fetchone()[0]
       
        jenis_tiket = request.POST['jenis_tiket']
        jenis_pembayaran = request.POST['jenis_pembayaran']

       
        cursor.execute(f"""
        INSERT INTO PEMBELIAN_TIKET VALUES ('{nomor_receipt}', '{id_penonton}', '{jenis_tiket}', '{jenis_pembayaran}', '{id_pertandingan}');
        """)

        return redirect("/dashboard/dashboard_penonton/")
