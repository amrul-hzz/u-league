from django.shortcuts import render

# Create your views here.
from .models import Pertandingan

def list_pertandingan(request):
    pertandingan = Pertandingan.objects.all()
    return render(request, 'list_pertandingan.html', {'pertandingan': pertandingan})

def buat_pertandingan(request):
    # Implementasikan logika untuk pembuatan pertandingan
    # Misalnya, Anda dapat menggunakan perintah Pertandingan.objects.create()

    return render(request, 'buat_pertandingan.html')

def batalkan_peminjaman(request, waktu, stadium):
    try:
        pertandingan = Pertandingan.objects.get(waktu=waktu, stadium=stadium)
        # Logika pembatalan peminjaman
        # Misalnya, Anda dapat menghapus entri peminjaman dengan perintah pertandingan.delete()
        return render(request, 'berhasil.html')  # Menampilkan halaman berhasil
    except Pertandingan.DoesNotExist:
        return render(request, 'gagal.html')  # Menampilkan halaman gagal

def validate_jadwal_tim_wasit(value):
    pertandingan = Pertandingan.objects.filter(waktu=value)
    if pertandingan.exists():
        raise ValidationError(_('Tim atau wasit sudah dijadwalkan pada pertandingan lain.'))
