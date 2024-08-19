from django.shortcuts import render, redirect
from .forms import TranslationForm
from .translation_model import extract_text_and_image_from_pdf, translate_text, save_text_and_image_to_pdf

def home(request):
    return render(request, 'home.html')

def translate_pdf_view(request):
    if request.method == 'POST':
        form = TranslationForm(request.POST, request.FILES)
        if form.is_valid():
            pdf_file = form.cleaned_data['pdf_file']
            direction = form.cleaned_data['direction']
            src_lang, tgt_lang = direction.split('-')

            # Save the uploaded PDF temporarily to extract its content
            with open(pdf_file.name, 'wb+') as temp_file:
                for chunk in pdf_file.chunks():
                    temp_file.write(chunk)

            # Extract text and image from the uploaded PDF
            text, image = extract_text_and_image_from_pdf(temp_file.name)

            # Translate the text
            translated_text = translate_text(text, src_lang, tgt_lang)

            # Save the translated text and image to a new PDF
            output_path = f"translated_{pdf_file.name}"
            save_text_and_image_to_pdf(translated_text, image, output_path)

            # Redirect to the success page with the file path as a query parameter
            return redirect(f'/Laws/translation_success/?file_path={output_path}')
    else:
        form = TranslationForm()

    return render(request, 'translate_pdf.html', {'form': form})

def translation_success_view(request):
    file_path = request.GET.get('file_path')
    download_url = f"/Laws/download_file/?file_path={file_path}"
    return render(request, 'translation_success.html', {'download_url': download_url})







    




    


     # Now you can save `output_path` to your database if needed
            # Example: Saving to a database model (assuming you have a Translation model)
            # translation_instance = Translation.objects.create(
            #     original_file=pdf_file.name,
            #     translated_file=output_filename,
            #     direction=direction
            # )
            # translation_instance.save()