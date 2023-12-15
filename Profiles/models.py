from django.db import models

class UserDetail(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=255)
    user_email = models.EmailField(unique=True)
    user_password = models.CharField(max_length=255)

    def __str__(self):
        return self.user_name

class PDF_Details(models.Model):
    pdf_id = models.AutoField(primary_key=True)
    pdf_name = models.CharField(max_length=255)
    pdf_vectordb_path = models.CharField(max_length=255)
    pdf_file = models.FileField(upload_to='pdf_files/')

    def __str__(self):
        return self.pdf_name