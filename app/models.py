from PIL import Image as Img

from io import StringIO, BytesIO 

from django.core.files.uploadedfile import InMemoryUploadedFile

from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from ckeditor_uploader.fields import RichTextUploadingField
from django.urls import reverse
import random
import string
from django.utils.text import slugify
from django.db.models.signals import post_save,pre_save
from .utils import unique_slug_generator




class UserDetail(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_image=models.ImageField(upload_to='profile_image',default='profileimage.png',blank=True)
    email=models.EmailField()
    biography=models.TextField()

    def __str__(self):
        return f"user name is--{self.user}"



class Category(models.Model):
    name=models.CharField(max_length=255)
    def __str__(self):
        return f"field names are {self.name}"
    def get_absolute_url(self):
        return reverse('home')

class BlogPost(models.Model):
    author=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    post_title=models.CharField(max_length=300,null=True,blank=True)
    category=models.CharField(max_length=255,default="World")
    post_image=models.ImageField(upload_to='postimages',default='post.png',blank=True,null=True)
    video=models.FileField(upload_to='postvideos', default='post.video',null=True,blank=True)
    thumbnail=models.ImageField(upload_to='thumbnailimages',default='thumbnail.png')
    content=RichTextUploadingField()
    slug=models.SlugField(max_length=2000,blank=True,unique=True)
    intro=models.CharField(max_length=300)
    likes=models.ManyToManyField(User,related_name='post_likes',blank=True)
    unlikes=models.ManyToManyField(User,related_name="post_unlikes",blank=True)
    featured=models.BooleanField(default=False)
    updated=models.DateTimeField(auto_now=True)
    created=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author}"
    

    def save(self,*args,**kwargs):
        if self.thumbnail:
            img=Img.open(BytesIO(self.thumbnail.read()))
            if img.mode!='RGB':
                img=img.convert('RGB')
            img.thumbnail((self.thumbnail.width/1.5,self.thumbnail.height/1.5),Img.ANTIALIAS)
            output=BytesIO()
            img.save(output,format='WebP',quality=60)
            output.seek(0)
            self.thumbnail=InMemoryUploadedFile(output,'ImageField',"%s.webp" %self.thumbnail.name.split('.')[0],'thumbnail/webp',len(output.getbuffer()),None)
        original_slug=slugify(self.intro)
        queryset=BlogPost.objects.all().filter(slug__iexact=original_slug).count()
        count=1
        slug=original_slug
        while(queryset):
            slug=original_slug+'-'+str(count)
            count+=1
            queryset=BlogPost.objects.all().filter(slug__iexact=slug).count()
        self.slug=slug
        if self.featured:
            try:
                temp=BlogPost.objects.get(featured=True)
                if self!=temp:
                    temp.featured=False
                    temp.save()
            except BlogPost.DoesNotExist:
                pass
        super().save(*args,**kwargs)
    def __str__(self):
        return f"{self.intro}"


    def get_absolute_url(self):
        return reverse('article-detail',kwargs={'slug':self.slug})
    def number_of_likes(self):
        return self.likes.all().count()
    def number_of_unlikes(self):
        return self.unlikes.all().count()





