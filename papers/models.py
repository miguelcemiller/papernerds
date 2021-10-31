from django.db import models
import uuid

# Create your models here.

class Paper(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True)
    abstract = models.TextField(blank=True, null=True)
    year = models.CharField(max_length=500, blank=True, null=True)
    downloads = models.IntegerField(blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self): 
        return str(self.title)    
