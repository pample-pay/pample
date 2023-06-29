from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('api/v1/map-data', views.DrugstoreInfo.as_view(), name='map_data'), 
]