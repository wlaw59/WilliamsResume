from django.contrib import admin
from .models import *
# Register your models here.
# giving admin permission to the Comments and Users table
admin.site.register(Users)
admin.site.register(Comments)
