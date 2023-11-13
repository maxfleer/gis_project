from django.contrib import admin
from .models import Location, UserData

# Register your models here.

admin.site.register(Location)
admin.site.register(UserData)

# Current users:

# Username: admin
# Password: 1234

# Username: testing
# Password: Passwort12345