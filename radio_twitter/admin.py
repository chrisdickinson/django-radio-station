from django.contrib import admin
from models import Credential
class CredentialAdmin(admin.ModelAdmin):
    list_display = ['username', 'is_active']
    list_filter = ['is_active',]
admin.site.register(Credential, CredentialAdmin)
