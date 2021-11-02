from django.db import models
from django.template.defaultfilters import slugify
from ckeditor_uploader.fields import RichTextUploadingField
# Create your models here.
class Contact(models.Model):
    count=models.AutoField(primary_key=True)
    name=models.CharField(max_length=1000)
    phone=models.CharField(max_length=20)
    email=models.EmailField(max_length=1000)
    description=models.TextField()
    timestamp=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Contact name is::{self.name}-contact-email-is-{self.email}-contact-time-is-{self.timestamp}"

class Image(models.Model):
    title=models.CharField(max_length=500)
    image=models.ImageField(upload_to='contactbackground',default='contact.png',blank=True,null=True)

    def __str__(self):
        return f"{self.title}"

class About(models.Model):
    aboutus=RichTextUploadingField()
