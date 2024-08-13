from django.urls import path
from .views import home, translate_pdf_view, translation_success_view  # Import views directly

urlpatterns = [
    path('', home, name='home'),  # Use the view name directly
    path('translate/', translate_pdf_view, name='translate'),  # Use the view name directly
    path('success/', translation_success_view, name='translation_success'),  # Use the view name directly
]
