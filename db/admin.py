from .models import DRUGSTORE_TB, DRUGSTORE_VIEW_TB
from django.contrib import admin


class DrugstoreAdmin(admin.ModelAdmin):
    list_display = (
        'drugstore_name', 
        'drugstore_areacode',
        'drugstore_citycode',

        'drugstore_zipcode',
        'drugstore_address',
        'drugstore_hp',
        'drugstore_open',
        'drugstore_lng',
        'drugstore_lat',
        'drugstore_associate',
        )
    search_fields = ('drugstore_name',)

admin.site.register(DRUGSTORE_TB, DrugstoreAdmin)


class DrugstoreViewAdmin(admin.ModelAdmin):
    list_display = (
        'drugstore', 

        )
    search_fields = ('drugstore',)

admin.site.register(DRUGSTORE_VIEW_TB, DrugstoreViewAdmin)
