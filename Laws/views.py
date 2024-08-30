# views.py

from django.shortcuts import render, redirect
from django.http import FileResponse, HttpResponse
from .forms import TranslationForm
from .translation_model import extract_text_and_image_from_pdf, translate_text, save_text_and_image_to_pdf
import os
from django.conf import settings
import sacrebleu

def home(request):
    return render(request, 'home.html')

def translate_pdf_view(request):
    if request.method == 'POST':
        form = TranslationForm(request.POST, request.FILES)
        if form.is_valid():
            pdf_file = form.cleaned_data['pdf_file']
            direction = form.cleaned_data['direction']
            src_lang, tgt_lang = direction.split('-')

            # Save the uploaded PDF
            upload_path = os.path.join(settings.MEDIA_ROOT, 'uploads', pdf_file.name)
            os.makedirs(os.path.dirname(upload_path), exist_ok=True)
            with open(upload_path, 'wb+') as temp_file:
                for chunk in pdf_file.chunks():
                    temp_file.write(chunk)

            # Extract text and image from the uploaded PDF
            text, image = extract_text_and_image_from_pdf(upload_path)

            # Translate the text
            translated_text = translate_text(text, src_lang, tgt_lang)

            # Tokenize the reference and candidate texts
            reference_texts = [text]  # List containing the original text
            candidate_texts = [translated_text]  # List containing the translated text

            # Calculate SacreBLEU score
            bleu_score = sacrebleu.corpus_bleu(
                candidate_texts,  # List of candidate texts
                [reference_texts]  # List containing a list of reference texts
            ).score

            # Save the translated text and image to a new PDF
            output_filename = f"translated_{pdf_file.name}"
            output_path = os.path.join(settings.MEDIA_ROOT, 'downloads', output_filename)
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            save_text_and_image_to_pdf(translated_text, image, output_path)

            # Redirect to the success page with the file path and BLEU score
            return redirect(f'/Laws/translation_success/?file_path={output_filename}&bleu_score={bleu_score:.2f}')
    else:
        form = TranslationForm()

    return render(request, 'translate_pdf.html', {'form': form})

def translation_success_view(request):
    file_path = request.GET.get('file_path')
    bleu_score = request.GET.get('bleu_score')
    download_url = f"/Laws/download_file/?file_path={file_path}"
    return render(request, 'translation_success.html', {'download_url': download_url, 'bleu_score': bleu_score})

def download_file_view(request):
    file_path = request.GET.get('file_path')
    download_path = os.path.join(settings.MEDIA_ROOT, 'downloads', file_path)
    try:
        return FileResponse(open(download_path, 'rb'), as_attachment=True)
    except Exception as e:
        print(f"Error serving file for download: {e}")
        return HttpResponse(f"Error serving file for download: {e}", status=500)













































    




    


     # Now you can save `output_path` to your database if needed
            # Example: Saving to a database model (assuming you have a Translation model)
            # translation_instance = Translation.objects.create(
            #     original_file=pdf_file.name,
            #     translated_file=output_filename,
            #     direction=direction
            # )
            # translation_instance.save()