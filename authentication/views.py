from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.db import connection
from django.contrib import messages

from django.views.decorators.csrf import csrf_exempt
from pprint import pprint
from dashboard.views import *

def landing(request):
    return render(request, 'landing.html')

def landing_register(request):
    return render(request, 'landing-register.html')

def login(request):
    response = {}
    response['error'] = False

    if(request.method == "POST"):
        response['username'] = request.POST['username']
        response['password'] = request.POST['password']
        if(verified(response)):
            request.session['username'] = response['username']
            if(is_manajer(response['username'])):
                request.session['role'] = 'manajer'
                return redirect('dashboard:show_dashboard_manajer')
            elif(is_panitia(response['username'])):
                request.session['role'] = 'panitia'
                return redirect('dashboard:show_dashboard_panitia')
            else:
                request.session['role'] = 'penonton'
                return redirect('dashboard:show_dashboard_penonton')
        else:
            response['error'] = True

    return render(request,'login.html',response)

def verified(data):
    query = """
    SELECT * FROM user_system;
    """
    cursor = connection.cursor()
    cursor.execute(query)

    user_data = fetch(cursor)
    for users in user_data:
        username_status = data['username'] == users['username']
        password_status = data['password'] == users['password']
        if(username_status and password_status):
            return True
    return False

def fetch(cursor):
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

def is_manajer(username_input):
    query = """
    SELECT username FROM manajer;
    """
    cursor = connection.cursor()
    cursor.execute(query)

    usernames = fetch(cursor)
    for username in usernames:
        if(username_input == username['username']):
            return True
    return False

def is_panitia(username_input):
    query = """
    SELECT username FROM panitia;
    """
    cursor = connection.cursor()
    cursor.execute(query)

    usernames = fetch(cursor)
    for username in usernames:
        if(username_input == username['username']):
            return True
    return False

def is_penonton(username_input):
    query = """
    SELECT username FROM penonton;
    """
    cursor = connection.cursor()
    cursor.execute(query)

    usernames = fetch(cursor)
    for username in usernames:
        if(username_input == username['username']):
            return True
    return False

# register penonton
def register_penonton(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        id_penonton = request.POST.get('id_penonton')
        nama_depan = request.POST.get('nama_depan')
        nama_belakang = request.POST.get('nama_belakang')
        nomor_hp = request.POST.get('nomor_hp')
        email = request.POST.get('email')
        alamat = request.POST.get('alamat')
        # debug all
        print(username, password, id_penonton, nama_depan, nama_belakang, nomor_hp, email, alamat)

        if (id_penonton != "" and username != "" and password != ""):
            with connection.cursor() as cursor:
                try:
                    cursor.execute(f'''
                        INSERT INTO USER_SYSTEM VALUES ('{username}', '{password}');
                        INSERT INTO NON_PEMAIN VALUES ('{id_penonton}', '{nama_depan}', '{nama_belakang}', '{nomor_hp}', '{email}', '{alamat}');
                        INSERT INTO PENONTON VALUES ('{id_penonton}', '{username}');
                    ''')

                    response = HttpResponse()
                    response.set_cookie('username', username)
                    response.set_cookie('password', password)
                    response.status_code = 200

                    show_dashboard_penonton(request)
                    return response
                
                except Exception as e:
                    print(e)
                    res = str(e).split('\n')[0]
                    messages.error(request, res)
        else:   
            messages.error(request, "Please fill all the fields")
    return render(request, 'cru_penonton_regis.html', {})

# show form register penonton
def show_register_penonton(request):
    return render(request, 'cru_penonton_regis.html', {})