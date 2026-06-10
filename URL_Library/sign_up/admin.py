from django.contrib import admin
from .models import User, UserContent

# Register your models here.
admin.site.register(User)
admin.site.register(UserContent)
