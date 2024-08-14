from django.shortcuts import render
from .forms import TranslationForm
from .translation_model import extract_text_and_image_from_pdf, translate_text, save_text_and_image_to_pdf
import os
from django.conf import settings
from django.http import HttpResponse

def home(request):
    return render(request, 'home.html')

def translate_pdf_view(request):
    if request.method == 'POST':
        form = TranslationForm(request.POST, request.FILES)
        if form.is_valid():
            pdf_file = form.cleaned_data['pdf_file']
            direction = form.cleaned_data['direction']
            src_lang, tgt_lang = direction.split('-')

            # Save the uploaded PDF temporarily
            temp_file_path = os.path.join(settings.MEDIA_ROOT, pdf_file.name)
            with open(temp_file_path, 'wb+') as temp_file:
                for chunk in pdf_file.chunks():
                    temp_file.write(chunk)

            # Extract text and image from the uploaded PDF
            text, image = extract_text_and_image_from_pdf(temp_file_path)

            # Translate the text
            translated_text = translate_text(text, src_lang, tgt_lang)

            # Save the translated text and image to a new PDF
            output_filename = f"translated_{pdf_file.name}"
            output_path = os.path.join(settings.MEDIA_ROOT, output_filename)
            save_text_and_image_to_pdf(translated_text, image, output_path)

            # Now you can save `output_path` to your database if needed
            # Example: Saving to a database model (assuming you have a Translation model)
            # translation_instance = Translation.objects.create(
            #     original_file=pdf_file.name,
            #     translated_file=output_filename,
            #     direction=direction
            # )
            # translation_instance.save()

            # Pass the file path to the success page
            return render(request, 'translation_success.html', {'file_path': output_path})

    else:
        form = TranslationForm()

    return render(request, 'translate_pdf.html', {'form': form})

def translation_success_view(request):
    # Assuming the translated file is stored in this location
    file_path = os.path.join("C:/Users/User/MalaysianGovt", "translated_document.pdf")
    
    # Create the download URL for the translated document
    download_url = f'/download/{os.path.basename(file_path)}'

    return render(request, 'translation_success.html', {
        'download_url': download_url
    })

def download_translated_document(request, filename):
    file_path = os.path.join("C:/Users/User/MalaysianGovt", filename)
    
    with open(file_path, 'rb') as file:
        response = HttpResponse(file.read(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response