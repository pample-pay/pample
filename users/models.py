from .choices import *

from db.models import DRUGSTORE_TB
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager):
    def create_user(self, user_id, password, **extra_fields):
        user = self.model(
            user_id = user_id,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, user_id, password):
        user = self.create_user(user_id, password)
        user.is_superuser = True
        user.is_staff = True
        user.is_admin = True
        user.user_type = 0
        user.save(using=self._db)
        return user
    

class User(AbstractBaseUser, PermissionsMixin):
    
    objects = UserManager()

    user_id = models.CharField(max_length=17, verbose_name="아이디", unique=True)
    password = models.CharField(max_length=256, verbose_name="비밀번호")
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name='가입일', null=True, blank=True)
    
    user_name = models.CharField(max_length=17, verbose_name="이름")
    user_type = models.CharField(choices=TYPE_CHOICES, max_length=18, verbose_name="등급", default=2)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'user_id'

    def __str__(self):
        return self.user_id

    class Meta:
        db_table = "회원목록"
        verbose_name = "모든 사용자"
        verbose_name_plural = "모든 사용자"


# 유저에서 cascade를 받아 세가지로 분류
# 일반 유저
class NormalUser(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    hp = models.CharField(max_length=11, verbose_name="휴대폰번호", unique=True, null=True, blank=True, default=None)

    def __str__(self):
        return self.user.user_id

    class Meta:
        db_table = "일반회원목록"
        verbose_name = "일반 회원"
        verbose_name_plural = "일반 회원"


# 약사 유저
class Pharmacist(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    store = models.ForeignKey(
        DRUGSTORE_TB,
        on_delete=models.CASCADE,
        null=True, blank=True, default=None
    )

    def __str__(self):
        return self.user.user_id

    class Meta:
        db_table = "약사회원목록"
        verbose_name = "약사 회원"
        verbose_name_plural = "약사 회원"

# 팜플 직원
class ParmStaff(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.user.user_id

    class Meta:
        db_table = "팜베이스회원목록"
        verbose_name = "팜베이스 회원"
        verbose_name_plural = "팜베이스 회원"