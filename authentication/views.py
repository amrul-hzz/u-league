from django.shortcuts import render, redirect
from django.db import connection
from pprint import pprint

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

def logout(request):
    next = request.GET.get("next")

    if not verified(request):
        return redirect("/")

    request.session.flush()
    request.session.clear_expired()

    if next != None and next != "None":
        return redirect(next)
    else:
        return redirect("/")

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