from django.contrib import admin
from .models import Location, UserData, UserDataManager

# Register your models here.

admin.site.register(Location)
admin.site.register(UserData)