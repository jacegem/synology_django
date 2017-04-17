from django.contrib import admin
from .models import Magnet

# Register your models here.


class MagnetAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Magnet._meta.fields]

admin.site.register(Magnet, MagnetAdmin)

