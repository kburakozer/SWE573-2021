from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.




class Tag(models.Model):
    
    def __str__(self):
        return self.tag_name

    tag_name = models.CharField(max_length=2000)
    tag_url = models.CharField(max_length=2000)

    #document = models.ForeignKey(to=Document, on_delete=models.CASCADE)

    


class Document(models.Model):

    def __str__(self):
        return self.title

      
    doc_id = models.CharField(max_length=200,blank=True)
    title = models.TextField(max_length=2000,blank=True)
    author = models.CharField(max_length=5000,blank=True)
    year = models.CharField(max_length=200,blank=True)
    abstract = models.TextField(max_length=10000,blank=True)
    tags = models.ManyToManyField(Tag)
    tokens = ArrayField(models.TextField(max_length=10000, blank=True, default=''), null=True)
    keywords = ArrayField(models.TextField(max_length=1000, blank=True, default=''), null=True)
    doi = models.CharField(max_length=2000,blank=True)