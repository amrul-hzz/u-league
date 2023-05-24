from django.shortcuts import render, redirect
from django.db import connection
from django.contrib import messages
from django.http import HttpResponse
from authentication.views import *

# Create your views here.
def pilih_stadium(request):
    if is_penonton(request.session['username']) == False:
        return HttpResponse('bukan penonton')
    
    # get stadium name and id
    cursor = connection.cursor()
    cursor.execute(f"""
    SELECT * FROM STADIUM
    """)
    
    stadium_id = cursor.fetchall()[0]
    stadium_name = cursor.fetchall()[1]
    stadium_list = []
    for i in range(0, len(stadium_id)):
        stadium_list.append([stadium_id[i], stadium_name[i]])
    
    context = {
        'stadium_list': stadium_list,
    }

    return render(request, "pilih_stadium.html", context)

def list_waktu_dan_pertandingan(request):
     if is_penonton(request.session['username']) == False:
        return HttpResponse('bukan penonton')
     cursor = connection.cursor()

     if request.method == "POST":
        stadium_id = request.POST.get("stadium")
        date = request.POST.get("date")

        # get stadium name
        cursor.execute(f"""
        SELECT * FROM STADIUM 
        WHERE ID_stadium = {stadium_id}
        """)
        stadium_name = cursor.fetchone()[1]

        # get hours
        cursor.execute(f"""
        SELECT ID_Pertandingan,Start_Datetime, End_Datetime
        FROM PERTANDINGAN
        WHERE {date} BETWEEN Start_datetime AND End_datetime
        """)
        rows = cursor.fetchall()
        match_list = []
        for i in range (0, len(rows)):
            id_pertandingan = rows[0]
            start = rows[1]
            end = rows[2]
            match_list.append([id_pertandingan, start, end])
        
        # get playing teams
        for match in match_list:
            id_pertandingan = match[0]
            cursor.execute(f"""
            SELECT Nama_Tim
            FROM TIM_PERTANDINGAN
            WHERE ID_Pertandingan = {id_pertandingan}
            """)
            rows = cursor.fetchall()
            team1 = rows[0]
            team2 = rows[1]
            match.append(team1, team2)
        
        context = {
            "stadium_name": stadium_name,
            "match_list": match_list
        }

        return render(request, 'list_waktu_dan_pertandingan.html', context)
     
def beli_tiket(request, id_pertandingan):
    
     