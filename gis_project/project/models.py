from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager

# Create your models here.

class UserDataManager (UserManager):
    pass

class UserData (AbstractUser):
    class Meta:
        verbose_name_plural = 'UserData'

    number_of_games_played = models.IntegerField(default= 0)
    sum_of_points = models.BigIntegerField(default= 0)



class Location (models.Model):
    location_name = models.CharField(max_length=128)
    longitude = models.DecimalField(max_digits=9,decimal_places=6)
    latitude = models.DecimalField(max_digits=9,decimal_places=6)
    picture_name_1 = models.CharField(max_length=256)
    picture_name_2 = models.CharField(max_length=256)
    picture_name_3 = models.CharField(max_length=256)
    picture_name_4 = models.CharField(max_length=256)
