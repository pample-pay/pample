from .models import DRUGSTORE
from django.contrib import admin


class DrugstoreAdmin(admin.ModelAdmin):
    list_display = (
        'drugstore_name', 
        'drugstore_zipcode',
        'drugstore_address',
        'drugstore_open',
        # 'drugstore_lng',
        # 'drugstore_lat',
        'drugstore_associate',
        )
    search_fields = ('drugstore_name',)

admin.site.register(DRUGSTORE, DrugstoreAdmin)