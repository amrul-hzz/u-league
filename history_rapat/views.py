from django.shortcuts import render, redirect
from django.db import connection
from django.contrib import messages
from django.http import HttpResponse
from authentication.views import *


def history_rapat(request):
    if is_manajer(request.session['username']) == True:

        # get id
        cursor = connection.cursor()
        cursor.execute(f"""
        SELECT ID_Pertandingan FROM RAPAT;
        """)
        id_pertandingan = cursor.fetchall()

        # get playing teams
        team1 = []
        team2 = []
        for id in id_pertandingan:
            id = id[0]

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
            id = id[0]

            cursor = connection.cursor()
            cursor.execute(f"""
            SELECT Stadium FROM PERTANDINGAN
            WHERE ID_Pertandingan = '{id}';
            """)
            stadium_id.append(cursor.fetchone())
        
        stadium_name = []
        for id in stadium_id:
            id = id[0]

            cursor = connection.cursor()
            cursor.execute(f"""
            SELECT Nama FROM STADIUM
            WHERE ID_Stadium = '{id}';
            """)
            stadium_name.append(str(cursor.fetchone()[0]))

        # get start 
        cursor = connection.cursor()
        cursor.execute(f"""
        SELECT Datetime FROM RAPAT;
        """)
        start = cursor.fetchall()
        start = [x[0] for x in start]

        # combine data
        rapat_list = []
        for i in range (0, len(id_pertandingan)):
            rapat = [team1[i], team2[i], stadium_name[i], start[i]]
            print("$$$ rapat: ", rapat )
            rapat_list.append(rapat)

        context = {
            "rapat_list": rapat_list
        }

        return render(request, 'history_rapat.html', context)
    else:
        return HttpResponse('bukan manajer')