from django.contrib import admin

# Register your models here.
from .models import Region, Districts

admin.site.register(Region)
admin.site.register(Districts)