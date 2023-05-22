from django.shortcuts import render

# Create your views here.
from .models import Pertandingan

def batalkan_peminjaman(request, waktu, stadium):
    try:
        pertandingan = Pertandingan.objects.get(waktu=waktu, stadium=stadium)
        # Logika pembatalan peminjaman
        # Misalnya, Anda dapat menghapus entri peminjaman dengan perintah pertandingan.delete()
        return render(request, 'berhasil.html')  # Menampilkan halaman berhasil
    except Pertandingan.DoesNotExist:
        return render(request, 'gagal.html')  # Menampilkan halaman gagal
