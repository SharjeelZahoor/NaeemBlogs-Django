from django.db import models
from django.contrib.auth.models import User
from datetime import datetime  

now =  datetime.now()
time = now.strftime("%d %B %Y")
# Create your models here.

# for validation
from django.core.exceptions import ValidationError
import os

def validate_file_type(value):
    ext = os.path.splitext(value.name)[1]  # Get the file extension
    valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.mp4', '.mov', '.avi']
    if ext.lower() not in valid_extensions:
        raise ValidationError('Unsupported file extension.')

class Post(models.Model):
    postname = models.CharField(max_length=600)
    category = models.CharField(max_length=600)
    image = models.FileField(upload_to='images/posts', validators=[validate_file_type])
    content = models.CharField(max_length=100000)
    time = models.CharField(default=time,max_length=100, blank=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    social_image = models.ImageField(upload_to='social_images/', null=True, blank=True)
    social_title = models.CharField(max_length=255, null=True, blank=True)
    meta_description = models.TextField(null=True, blank=True)
    social_description = models.TextField(null=True, blank=True)
    meta_keywords = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return str(self.postname)

    def total_likes(self):
        return self.likes.count()


class Comment(models.Model):
    content = models.CharField(max_length=200)
    time = models.CharField(default=time,max_length=100, blank=True)
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    def __str__(self):
        return  f"{self.id}.{self.content[:20]}..."
    
    

class SocialMediaLink(models.Model):
    PLATFORM_CHOICES = [
        ('facebook', 'Facebook'),
        ('instagram', 'Instagram'),
        ('twitter', 'Twitter'),
        ('youtube', 'YouTube'),
        ('linkedin', 'LinkedIn'),
    ]
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES, unique=True)
    url = models.URLField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.platform.capitalize()} Link"
