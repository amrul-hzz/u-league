from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Pertandingan(models.Model):
    id_pertandingan = models.AutoField(primary_key=True)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    stadium = models.CharField(max_length=100)
    # Bidang-bidang lain yang Anda perlukan untuk model Pertandingan

    def __str__(self):
        return f'Pertandingan {self.start_datetime} di {self.stadium}'

class Wasit(models.Model):
    id_wasit = models.AutoField(primary_key=True)
    lisensi = models.CharField(max_length=100)

class Tim(models.Model):
    nama_tim = models.CharField(max_length=100, unique=True)
    universitas = models.CharField(max_length=100)

class Stadium(models.Model):
    id_stadium = models.AutoField(primary_key=True)
    nama = models.CharField(max_length=100)
    alamat = models.CharField(max_length=200)
    kapasitas = models.PositiveIntegerField()

class TimPertandingan(models.Model):
    id_pertandingan = models.ForeignKey(Pertandingan, on_delete=models.CASCADE)
    id_tim_1 = models.ForeignKey(Tim, on_delete=models.CASCADE)
    skor = models.IntegerField()
    # Bidang-bidang lain untuk model TimPertandingan

class WasitBertugas(models.Model):
    id_pertandingan = models.ForeignKey(Pertandingan, on_delete=models.CASCADE)
    wasit = models.ForeignKey(Wasit, on_delete=models.CASCADE)
    posisi_wasit = models.CharField(max_length=100)
