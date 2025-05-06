from django.db import models

class Document(models.Model):
    original_file = models.FileField(upload_to='documents/')
    converted_file = models.FileField(upload_to='converted/', blank=True, null=True)
    converted_format = models.CharField(max_length=10)
    uploaded_at = models.DateTimeField(auto_now_add=True)