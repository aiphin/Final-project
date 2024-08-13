from django.db import models

# Create your models here.
from django.db import models

class TranslatedPDF(models.Model):
    original_file = models.FileField(upload_to='originals/')
    translated_file = models.FileField(upload_to='translations/')
    src_lang = models.CharField(max_length=5)
    tgt_lang = models.CharField(max_length=5)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.src_lang} to {self.tgt_lang} translation on {self.created_at}"
