from django.contrib import admin
from .models import User, NormalUser, Pharmacist, ParmStaff
from django.contrib.auth.models import Group


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'user_id', 
        'date_joined',
        )
    search_fields = ('user_id', )

admin.site.register(User, UserAdmin)
admin.site.unregister(Group) # Admin페이지의 GROUP삭제


class NormalUserAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'hp',
        )
    search_fields = ('user',)

class PharmacistAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'store',
        )
    search_fields = ('user', 'store', )

class ParmStaffAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        )
    search_fields = ('user', )
    
    
admin.site.register(NormalUser, NormalUserAdmin)
admin.site.register(Pharmacist, PharmacistAdmin)
admin.site.register(ParmStaff, ParmStaffAdmin)