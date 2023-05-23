from django.shortcuts import render
from django.db import connection
from django.http import JsonResponse

def fetch(cursor):
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

def show_dashboard_penonton(request):
    response = {}
    query = f"""
    SELECT * FROM penonton
    JOIN non_pemain ON id_penonton = id
    WHERE id_penonton IN (
        SELECT id_penonton FROM penonton WHERE username = '{request.session['username']}'
    );"""

    cursor = connection.cursor()
    cursor.execute(query)
    user_data = fetch(cursor)

    for data in user_data:
        request.session['id'] = str(data['id'])
        response['nama_depan'] = data['nama_depan']
        response['nama_belakang'] = data['nama_belakang']
        response['nomor_hp'] = data['nomor_hp']
        response['email'] = data['email']
        response['alamat'] = data['alamat']

    query = f"""
    SELECT status FROM status_non_pemain
    WHERE id_non_pemain = '{request.session['id']}';"""
    cursor.execute(query)
    user_data = fetch(cursor)

    for data in user_data:
        response['status'] = data['status']

    return render(request, 'dashboard_penonton.html', response)

def show_dashboard(request):
    return render(request, "dashboard_manajer.html")

def show_dashboard_manajer(request):
    cursor = connection.cursor()
    cursor.execute(f"""
    SELECT *
    """)
    return render(request, 'dashboard_manajer.html')

def show_dashboard_panitia(request):
    return render(request, 'dashboard_panitia.html')
