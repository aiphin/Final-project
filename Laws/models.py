from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class TranslatedPDF(models.Model):
    original_file = models.FileField(upload_to='originals/')
    translated_file = models.FileField(upload_to='translations/')
    src_lang = models.CharField(max_length=5)
    tgt_lang = models.CharField(max_length=5)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.src_lang} to {self.tgt_lang} translation on {self.created_at}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Add any additional fields you need here
    # e.g. phone_number = models.CharField(max_length=15, blank=True)
    
    def __str__(self):
        return self.user.username

#this is final project