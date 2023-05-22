from django.urls import path
from .views import batalkan_peminjaman

urlpatterns = [
    path('batalkan/<waktu>/<stadium>/', batalkan_peminjaman, name='batalkan_peminjaman'),
]
