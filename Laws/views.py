from django.shortcuts import render, redirect
from django.http import HttpResponse, FileResponse
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.urls import reverse
import os
import logging
from .forms import TranslationForm, SignUpForm, LoginForm
from .models import TranslatedPDF
from .translation_model import extract_text_and_image_from_pdf, translate_text, save_text_and_image_to_pdf

# Initialize logger
logger = logging.getLogger(__name__)

def home(request):
    return render(request, 'home.html')

@login_required
def translate_pdf_view(request):
    if request.method == 'POST':
        form = TranslationForm(request.POST, request.FILES)
        if form.is_valid():
            pdf_file = form.cleaned_data['pdf_file']
            direction = form.cleaned_data['direction']
            src_lang, tgt_lang = direction.split('-')

            # Save the uploaded PDF to 'uploads' directory
            upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
            os.makedirs(upload_dir, exist_ok=True)
            fs = FileSystemStorage(location=upload_dir)
            filename = fs.save(pdf_file.name, pdf_file)
            uploaded_file_path = os.path.join(upload_dir, filename)

            logger.info(f"Uploaded file saved at {uploaded_file_path}")

            # Extract text and image from the uploaded PDF
            text, image = extract_text_and_image_from_pdf(uploaded_file_path)
            logger.info(f"Extracted text: {text[:100]}...")  # Log the first 100 characters

            # Translate the text
            translated_text = translate_text(text, src_lang, tgt_lang)
            logger.info(f"Translated text: {translated_text[:100]}...")  # Log the first 100 characters

            # Save the translated text and image to a new PDF in the 'downloads' directory
            base_filename = os.path.splitext(pdf_file.name)[0]
            output_filename = f"{base_filename}_translated.pdf"
            output_path = save_text_and_image_to_pdf(translated_text, image, output_filename)

            # Save to TranslatedPDF model
            translated_pdf_instance = TranslatedPDF(
                original_file=filename,
                translated_file=output_filename,
                src_lang=src_lang,
                tgt_lang=tgt_lang
            )
            translated_pdf_instance.save()

            # Redirect with the download URL as a query parameter
            download_url = f"{settings.MEDIA_URL}downloads/{output_filename}"
            return redirect(f"{reverse('translation_success')}?download_url={download_url}")
        else:
            logger.error("Form is not valid")
    else:
        form = TranslationForm()
    return render(request, 'translate_pdf.html', {'form': form})

@login_required
def download_file_view(request):
    file_path = request.GET.get('file_path', None)
    if file_path:
        file_path = os.path.join(settings.MEDIA_ROOT, 'downloads', file_path)
        if os.path.exists(file_path):
            return FileResponse(open(file_path, 'rb'), as_attachment=True)
    return redirect('home')

def translation_success_view(request):
    download_url = request.GET.get('download_url', None)
    return render(request, 'translation_success.html', {'download_url': download_url})

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('signup_success')  # Redirect to the success page after signup
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def signup_success_view(request):
    return render(request, 'signup_success.html')

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('translate_pdf')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return render(request, 'logout.html')
#this is final project