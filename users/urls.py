from . import views

from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

app_name = 'users'

urlpatterns = [
    path("test_veiw/", views.test_veiw),

    path("register/", views.RegisterAPIView.as_view()), # 회원코드 : 일반회원-2, 약사회원-3, 팜베이스회원-4
    path("auth/", views.AuthAPIView.as_view()),
    path("auth/refresh/", TokenRefreshView.as_view()), # TokenRefeshView 에 refresh token 을 보내면 새로운 access token이 반환

    path("change_password/", views.ChangePassword.as_view()), 
    path("idvalidation/", views.IdValidation.as_view()),

    path("token/", views.TokenValidAPIView.as_view()),
]