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

def validate_jadwal_tim_wasit(value):
    pertandingan = Pertandingan.objects.filter(waktu=value)
    if pertandingan.exists():
        raise ValidationError(_('Tim atau wasit sudah dijadwalkan pada pertandingan lain.'))

class Tim(models.Model):
    waktu_pertandingan = models.DateTimeField(validators=[validate_jadwal_tim_wasit])
    # Bidang-bidang lain untuk model Tim

class Wasit(models.Model):
    waktu_pertandingan = models.DateTimeField(validators=[validate_jadwal_tim_wasit])
    # Bidang-bidang lain untuk model Wasit
