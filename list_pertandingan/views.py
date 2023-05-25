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
        id_pertandingan = str(cursor.fetchall())

        # get start 
        cursor = connection.cursor()
        cursor.execute(f"""
        SELECT Start_Datetime FROM PERTANDINGAN;
        """)
        start = cursor.fetchall()

        # get end
        cursor = connection.cursor()
        cursor.execute(f"""
        SELECT End_Datetime FROM PERTANDINGAN;
        """)
        end = cursor.fetchall()

        # get stadium id
        cursor = connection.cursor()
        cursor.execute(f"""
        SELECT ID_Stadium FROM PERTANDINGAN;
        """)
        stadium_id = str(cursor.fetchall())

        # get stadium name
        stadium_name = []
        for i in range (0, len(id_pertandingan)):
            cursor = connection.cursor()
            cursor.execute(f"""
            SELECT Nama FROM STADIUM
            WHERE ID_Stadium = {stadium_id[i]};
            """)
            stadium_name.append(str(cursor.fetchone()))
        
        # get playing teams
        team1 = []
        team2 = []
        for i in range(0, len(id_pertandingan)):
            cursor = connection.cursor()
            cursor.execute(f"""
            SELECT Nama_Tim FROM TIM_PERTANDINGAN
            WHERE ID_Pertandingan = {id_pertandingan[i]};
            """)
            team1.append(str(cursor.fetchall()[0]))
            team2.append(str(cursor.fetchall()[1]))

        # combine data
        match_list = []
        for i in range (0, len(id_pertandingan)):
            match = [team1[i], team2[i], stadium_name[i], start[i], end[i]]
            match_list.append(match)

        context = {
            "jenis_user": jenis_user,
            "match_list": match_list,
        }

        return render(request, 'list_pertandingan.html', context)
    
    else:
        return HttpResponse('bukan penonton ataupun manajer')