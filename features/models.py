from django.db import models
import uuid
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    
    firstname = models.CharField(max_length=200, blank=True, null=True)
    middleinitial = models.CharField(max_length=200, blank=True, null=True)
    lastname = models.CharField(max_length=200, blank=True, null=True)

    email = models.EmailField(max_length=500, blank=True, null=True)
    password = models.CharField(max_length=200, blank=True, null=True)

    profile_image = models.ImageField(null=True, blank=True, upload_to='profiles/')
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return str(self.user.username)

class Paper(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True)
    abstract = models.TextField(blank=True, null=True)
    year = models.CharField(max_length=500, blank=True, null=True)
    downloads = models.IntegerField(blank=True, null=True)
    pdf_name = models.CharField(max_length=200, blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self): 
        return str(self.title)    