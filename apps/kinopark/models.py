from django.db import models
from django.contrib.auth.models import AbstractUser



class Movie(models.Model):
    title = models.CharField(max_length=70, blank=False, default='')
    description = models.CharField(max_length=300, blank=False, default='')
    producer = models.CharField(max_length=50, blank=False, default='')
    rating = models.FloatField(blank=False)
    published = models.BooleanField(default=False)


class User(AbstractUser):
    first_name = models.CharField(max_length=80, blank=False)
    last_name = models.CharField(max_length=80, blank=False)
    email = models.CharField(max_length=90, blank=False, unique=True)
    username = models.CharField(max_length=90, blank=True, null=True, unique=True)
    password = models.CharField(max_length=90, blank=False)
    # username = None

    # USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []


class Order(models.Model):
    price = models.BigIntegerField(blank=False)
    time = models.DateTimeField(auto_now=True)
    movie = models.ForeignKey('Movie', on_delete=models.PROTECT)
    user = models.ForeignKey('User', on_delete=models.PROTECT)