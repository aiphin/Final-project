"""
URL configuration for MalaysianGovt project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Laws import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('translate/', views.translate_pdf_view, name='translate_pdf'),
    path('signup/', views.signup_view, name='signup'),
    path('signup_success/', views.signup_success_view, name='signup_success'),  # New URL for signup success
    path('translation_success/', views.translation_success_view, name='translation_success'),
    path('download_file/', views.download_file_view, name='download_file'),
    path('login/', views.login_view, name='login'),
    path('logout/', LogoutView.as_view(template_name='logout.html'), name='logout'),
]

# This will only serve media files during development.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#this is final project
