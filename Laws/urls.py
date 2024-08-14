from django.urls import path
from .views import download_translated_document, home, translate_pdf_view, translation_success_view  # Import views directly

urlpatterns = [
    path('', home, name='home'),  # Use the view name directly
    path('translate/', translate_pdf_view, name='translate'),  # Use the view name directly
    path('translation-successful/', translation_success_view, name='translation_successful'),
    path('download/<str:filename>/', download_translated_document, name='download_translated_document'),
]
