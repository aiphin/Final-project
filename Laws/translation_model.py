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
                if page_text:  # Check if there's any text on the page
                    text += page_text + "\n"

                # Extract the first image from the first page
                if page_num == 0 and not first_image:
                    images = page.images
                    if images:
                        image = images[0]
                        x0, y0, x1, y1 = image["x0"], image["y0"], image["x1"], image["y1"]
                        first_image = page.within_bbox((x0, y0, x1, y1)).to_image().original

        return text, first_image
    except Exception as e:
        print(f"Error extracting text or image from PDF: {e}")
        return None, None

def translate_text(text, src_lang, tgt_lang):
    try:
        translator = GoogleTranslator(source=src_lang, target=tgt_lang)
        translated_text = ""

        # Split the text into chunks of 5000 characters or less
        chunks = [text[i:i + 4999] for i in range(0, len(text), 4999)]
        
        for chunk in chunks:
            translated_text += translator.translate(chunk)
        
        return translated_text
    except Exception as e:
        print(f"Error during translation: {e}")
        return None

def save_text_and_image_to_pdf(text, image, output_filename):
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)

        # Add the image to the PDF (center-aligned)
        if image:
            # Convert image to a format that can be used by FPDF
            image_data = io.BytesIO(image)
            image_obj = Image.open(image_data)

            image_width, image_height = image_obj.size
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
            # Convert to an acceptable format for FPDF (JPEG or PNG)
            image_path = f"/tmp/{output_filename}.png"
            image_obj.save(image_path, format='PNG')
            pdf.image(image_path, x=x, y=pdf.get_y(), w=width, h=height)
            pdf.ln(height + 10)  # Add some space after the image

        # Add the translated text to the PDF
        lines = text.split('\n')
        for line in lines:
            if line.strip() == "":
                pdf.ln(10)  # Add a blank line for paragraph spacing
            else:
                if line.isupper():  # Assuming titles are in uppercase
                    pdf.set_font("Arial", "B", size=14)
                    pdf.multi_cell(0, 10, line, align="C")
                else:
                    encoded_line = line.encode('latin-1', 'replace').decode('latin-1')
                    pdf.set_font("Arial", size=12)
                    pdf.multi_cell(0, 10, encoded_line)

        # Define output path within the 'downloads' directory
        output_path = os.path.join(settings.MEDIA_ROOT, 'downloads', output_filename)
        pdf.output(output_path)
        print(f"PDF saved as {output_path}")

        # Clean up temporary image file
        if os.path.exists(image_path):
            os.remove(image_path)

        return output_path
    except Exception as e:
        print(f"Error saving PDF: {e}")
        return None
#this is final project
