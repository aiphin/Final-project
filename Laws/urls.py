from django.urls import path
from .views import home, translate_pdf_view, translation_success_view
from .translation_model import download_file_view

urlpatterns = [
    path('', home, name='home'),
    path('translate_pdf/', translate_pdf_view, name='translate_pdf'),
    path('translation_success/', translation_success_view, name='translation_success'),
    path('download_file/', download_file_view, name='download_file'),
]


