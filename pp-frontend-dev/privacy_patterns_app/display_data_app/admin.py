from django.contrib import admin
from .models import DataEntry, UserModel

# Register your models here.
admin.site.register(DataEntry)
admin.site.register(UserModel)
