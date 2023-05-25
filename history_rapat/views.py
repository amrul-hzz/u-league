from django.shortcuts import render, redirect
from django.db import connection
from django.contrib import messages
from django.http import HttpResponse
from authentication.views import *


def history_rapat(request):
    if is_manajer(request.session['username']) == True:

        # get meeting start time 
        cursor = connection.cursor()
        cursor.execute(f"""
        SELECT Datetime FROM RAPAT;
        """)
        start = cursor.fetchall()
        start = [x[0] for x in start]

        # get panitia id then nama_panitia
        id_panitia = []
        for s in start:
            cursor = connection.cursor()
            cursor.execute(f"""
            SELECT Perwakilan_Panitia FROM RAPAT
            WHERE Datetime = '{s}';
            """)
            id_panitia.append(str(cursor.fetchone()[0]))

        nama_panitia = []
        for id in id_panitia:
            cursor = connection.cursor()
            cursor.execute(f"""
            SELECT Nama_Depan FROM NON_PEMAIN
            WHERE ID = '{id}';
            """)
            nama_panitia.append(cursor.fetchone()[0])

        # get id pertandingan to get playing teams and stadium id then stadium name
        id_pertandingan = []
        for i in range (0, len(start)):
            cursor = connection.cursor()
            cursor.execute(f"""
            SELECT ID_Pertandingan FROM RAPAT
            WHERE Datetime = '{start[i]}' AND
                    Perwakilan_Panitia = '{id_panitia[i]}';
            """)
            id_pertandingan.append(str(cursor.fetchone()[0]))

        # get playing teams
        team1 = []
        team2 = []
        for id in id_pertandingan:
            cursor = connection.cursor()
            cursor.execute(f"""
            SELECT Nama_Tim FROM TIM_PERTANDINGAN
            WHERE ID_Pertandingan = '{id}';
            """)
            team1.append(cursor.fetchone()[0])
            team2.append(cursor.fetchone()[0])
        
        # get stadium id then stadium names
        stadium_id = []
        for id in id_pertandingan:
            cursor = connection.cursor()
            cursor.execute(f"""
            SELECT Stadium FROM PERTANDINGAN
            WHERE ID_Pertandingan = '{id}';
            """)
            stadium_id.append(str(cursor.fetchone()[0]))
        
        stadium_name = []
        for id in stadium_id:
            cursor = connection.cursor()
            cursor.execute(f"""
            SELECT Nama FROM STADIUM
            WHERE ID_Stadium = '{id}';
            """)
            stadium_name.append(str(cursor.fetchone()[0]))

        # combine data
        rapat_list = []
        for i in range (0, len(id_pertandingan)):
            rapat = [team1[i], team2[i], nama_panitia[i], stadium_name[i], start[i]]
            rapat_list.append(rapat)

        context = {
            "rapat_list": rapat_list
        }

        return render(request, 'history_rapat.html', context)
    else:
        return HttpResponse('bukan manajer')