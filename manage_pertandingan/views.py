from django.shortcuts import render

def show_manage_pertandingan_sebelum(request):
    query = """
    SELECT * FROM pertandingan;
    """
    
    return render(request, 'manage_pertandingan_sebelum.html')

def show_list_pertandingan_stage(request):
    return render(request, 'list_pertandingan_stage.html')

def show_list_pertandingan_nonstage(request):
    return render(request, 'list_pertandingan_nonstage.html')

def show_manage_pertandingan_sesudah(request):
    return render(request, 'manage_pertandingan_sesudah.html')

def show_lihat_peristiwa(request):
    return render(request, 'lihat_peristiwa.html')
