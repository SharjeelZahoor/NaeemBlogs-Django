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
    likes = models.IntegerField(null=True,blank=True,default=0)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    
    def __str__(self):
        return str( self.postname)
    
    
class Comment(models.Model):
    content = models.CharField(max_length=200)
    time = models.CharField(default=time,max_length=100, blank=True)
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    def __str__(self):
        return  f"{self.id}.{self.content[:20]}..."
    
    

class Contact(models.Model):
    name = models.CharField(max_length=600)
    email = models.EmailField(max_length=600)
    subject = models.CharField(max_length=1000)
    message = models.CharField(max_length=10000, blank=True)