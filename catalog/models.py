from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class Topic(models.Model):
    name = models.CharField(max_length=100)


class Redactor(AbstractUser):
    years_of_experience = models.IntegerField(null=True, blank=True)

class Newspaper(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    published_date = models.DateTimeField()
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    publishers = models.ManyToManyField(Redactor)
