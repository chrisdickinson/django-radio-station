from django.contrib import admin
from models import Ad

class AdAdmin(admin.ModelAdmin):
    list_display = ['name', 'image', 'link']

admin.site.register(Ad, AdAdmin)
