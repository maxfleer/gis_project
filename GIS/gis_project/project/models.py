from django.db import models

# Create your models here.

class UserData (models.Model):
    class Meta:
        verbose_name_plural = 'UserData'

    user_ID = models.IntegerField(default= -1)
    number_of_games_played = models.IntegerField(default= -1)
    sum_of_points = models.BigIntegerField(default= -1)



class Location (models.Model):
    location_name = models.CharField(max_length=64)
    longitude = models.DecimalField(max_digits=9,decimal_places=6)
    latitude = models.DecimalField(max_digits=9,decimal_places=6)
    picture_URL_1 = models.URLField(max_length=256)
    picture_URL_2 = models.URLField(max_length=256)
    picture_URL_3 = models.URLField(max_length=256)
    picture_URL_4 = models.URLField(max_length=256)
    hint_1 = models.CharField(max_length=512)
    hint_2 = models.CharField(max_length=512)
    hint_3 = models.CharField(max_length=512)

