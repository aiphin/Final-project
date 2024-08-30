import os
import pdfplumber
from deep_translator import GoogleTranslator
from fpdf import FPDF
from PIL import Image
import io
from django.conf import settings

def extract_text_and_image_from_pdf(pdf_path):
    text = ""
    first_image = None
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages):
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"

                # Extract the first image from the first page
                if page_num == 0 and not first_image:
                    images = page.images
                    if images:
                        image = images[0]
                        x0, y0, x1, y1 = image["x0"], image["y0"], image["x1"], image["y1"]
                        first_image = page.within_bbox((x0, y0, x1, y1)).to_image().original
    except Exception as e:
        print(f"Error extracting text or image from PDF: {e}")

    return text, first_image

def translate_text(text, src_lang, tgt_lang):
    translated_text = ""
    try:
        translator = GoogleTranslator(source=src_lang, target=tgt_lang)
        # Break text into chunks to avoid exceeding API limits
        chunks = [text[i:i + 4999] for i in range(0, len(text), 4999)]
        
        for chunk in chunks:
            translated_text += translator.translate(chunk)
    except Exception as e:
        print(f"Error during translation: {e}")

    return translated_text

def save_text_and_image_to_pdf(text, image, output_filename):
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)

        # Add image if it exists
        if image:
            image = Image.open(io.BytesIO(image))
            image_width, image_height = image.size
            pdf_width = pdf.w - 2 * pdf.l_margin
            pdf_height = pdf.h - 2 * pdf.t_margin
            aspect_ratio = image_width / image_height

            if aspect_ratio > 1:
                width = pdf_width
                height = pdf_width / aspect_ratio
            else:
                width = pdf_height * aspect_ratio
                height = pdf_height

            x = (pdf.w - width) / 2
            image_io = io.BytesIO()
            image.save(image_io, format='PNG')
            image_io.seek(0)
            pdf.image(image_io, x=x, y=pdf.get_y(), w=width, h=height)
            pdf.ln(height + 10)

        # Add text
        lines = text.split('\n')
        for line in lines:
            if line.strip() == "":
                pdf.ln(10)
            else:
                if line.isupper():
                    pdf.set_font("Arial", "B", size=14)
                    pdf.multi_cell(0, 10, line, align="C")
                else:
                    # Handle text encoding
                    encoded_line = line.encode('latin-1', 'replace').decode('latin-1')
                    pdf.set_font("Arial", size=12)
                    pdf.multi_cell(0, 10, encoded_line)
        
        output_path = os.path.join(settings.MEDIA_ROOT, 'downloads', output_filename)
        pdf.output(output_path)
        print(f"PDF saved as {output_path}")

    except Exception as e:
        print(f"Error saving PDF: {e}")
        return None

    return output_path


def download_file_view(request):
    file_path = request.GET.get('file_path')
    try:
        return FileResponse(open(file_path, 'rb'), as_attachment=True)
    except Exception as e:
        print(f"Error serving file for download: {e}")
        return None

