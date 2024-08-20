# Laws/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('translate_pdf/', views.translate_pdf_view, name='translate_pdf'),
    path('translation_success/', views.translation_success_view, name='translation_success'),
    path('download_file/', views.download_file_view, name='download_file'),
]




