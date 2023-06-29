from . import views

from django.urls import path

app_name = 'lists'

urlpatterns = [
    path('write/', views.BlogList.as_view()),
    path('<int:pk>/', views.ListDetail.as_view()),
]