from django.db import models
import uuid
from django.contrib.auth.models import User

from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify
import string
import random

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

    slug = models.SlugField(max_length=500, unique=True, null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self): 
        return str(self.title)    



STAGES = (
    ('pre_proposal', 'PRE-PROPOSAL'),
    ('proposal', 'PROPOSAL'),
    ('colloquium', 'COLLOQUIUM'),
    ('final_oral', 'FINAL-ORAL'),
)

class Portal(models.Model):
    step = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=200, blank=True, null=True)
    stage = models.CharField(max_length=20, choices=STAGES)
   
    slug = models.SlugField(max_length=500, unique=True, null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self): 
        return str(self.step) 




# Functions

# Random string generator
def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

# Unique slug generator
def unique_slug_generator(sender, instance, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        if sender == Paper:
            slug = slugify(instance.title)
        elif sender == Portal:
            slug = slugify(instance.step)

    class_ = instance.__class__
    qs_exists = class_.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = f"{slug}-{random_string_generator(size=5)}"
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug


@receiver(pre_save, sender=Paper)
def post_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(Paper, instance)

@receiver(pre_save, sender=Portal)
def post_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(Portal, instance)


