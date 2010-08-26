from django.contrib import admin
from .models import Role, StaffRoleRelation

class StaffRoleRelationAdmin(admin.ModelAdmin):
    list_display = ['role', 'user']
    list_filter = ['schedule', 'role']

admin.site.register(Role)
admin.site.register(StaffRoleRelation, StaffRoleRelationAdmin)
