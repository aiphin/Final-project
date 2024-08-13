from django import forms

class TranslationForm(forms.Form):
    pdf_file = forms.FileField(label='Select a PDF file')
    direction = forms.ChoiceField(
        choices=[('ms-en', 'Malay to English'), ('en-ms', 'English to Malay')],
        label='Translation Direction'
    )
