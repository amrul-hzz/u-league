from django.shortcuts import render, redirect
from django.db import connection
from django.contrib import messages
from django.http import HttpResponse
from authentication.views import *

def list_pertandingan(request):
    if is_penonton(request.session['username']) == True or is_manajer(request.session['username']) == True:

        jenis_user= 'manajer'
        if (is_penonton(request.session['username'])):
            jenis_user = 'penonton'

        # get id
        cursor = connection.cursor()
        cursor.execute(f"""
        SELECT ID_Pertandingan FROM PERTANDINGAN;
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
            team1.append(str(cursor.fetchone()[0]))
            team2.append(str(cursor.fetchone()[0]))

        # get stadium id then stadium name
        cursor = connection.cursor()
        cursor.execute(f"""
        SELECT Stadium FROM PERTANDINGAN;
        """)
        stadium_id = cursor.fetchall()

        stadium_name = []
        for id in stadium_id:
            id = id[0]

            cursor = connection.cursor()
            cursor.execute(f"""
            SELECT Nama FROM STADIUM
            WHERE ID_Stadium = '{id}';
            """)
            stadium_name.append(cursor.fetchone()[0])
          

        # get start 
        cursor = connection.cursor()
        cursor.execute(f"""
        SELECT Start_Datetime FROM PERTANDINGAN;
        """)
        start = cursor.fetchall()   
        start = [x[0] for x in start]     

        # get end
        cursor = connection.cursor()
        cursor.execute(f"""
        SELECT End_Datetime FROM PERTANDINGAN;
        """)
        end = cursor.fetchall()
        end = [x[0] for x in end]

        # combine data
        match_list = []
        for i in range (0, len(id_pertandingan)):
            match = [team1[i], team2[i], stadium_name[i], start[i], end[i]]
            match_list.append(match)

        context = {
            "jenis_user": jenis_user,
            "match_list": match_list,
        }

        print("context: ", context)

        return render(request, 'list_pertandingan_r.html', context)
    
    else:
        return HttpResponse('bukan penonton ataupun manajer')