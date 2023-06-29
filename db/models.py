from .choices import *
from django.db import models

# 약국 목록 테이블
class DRUGSTORE_TB(models.Model):
    drugstore_name = models.CharField(max_length=256, verbose_name="약국명")
    drugstore_areacode = models.IntegerField(choices=AREACODE_CHOICES, verbose_name="시도코드")
    drugstore_citycode = models.IntegerField(choices=CITYCODE_CHOICES, verbose_name="시군구코드")

    drugstore_zipcode = models.IntegerField(verbose_name="우편번호")
    drugstore_address = models.CharField(max_length=256, verbose_name="주소")
    drugstore_hp = models.CharField(max_length=256, verbose_name="전화번호", null=True, blank=True)
    drugstore_open = models.CharField(max_length=256, verbose_name="개설일자", null=True, blank=True)

    drugstore_lng = models.FloatField(verbose_name="경도", null=True)
    drugstore_lat = models.FloatField(verbose_name="위도", null=True)

    drugstore_associate = models.IntegerField(choices=ASSOCIATE_CHOICES,
                                              default = '0',
                                              verbose_name="제휴여부")

    def __str__(self):
        return str(self.id)
    
    class Meta:
        db_table = "DRUGSTORE_TB"
        verbose_name = "약국정보"
        verbose_name_plural = "약국정보"
        

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

# 약국 정보 페이지 리스트 보기
class DRUGSTORE_VIEW_TB(models.Model):
    drugstore = models.OneToOneField(DRUGSTORE_TB, on_delete=models.CASCADE, primary_key=True)

    drugstore_thumbnail = models.CharField(max_length=256, verbose_name="이미지주소")
    drugstore_abstract = models.TextField(verbose_name='소개글', null=True, blank=True)
    drugstore_content = models.TextField(verbose_name='내용', null=True, blank=True)

    def __str__(self):
        return str(self.drugstore)
    
    class Meta:
        db_table = "DRUGSTORE_VIEW_TB"
        verbose_name = "약국소개 페이지"
        verbose_name_plural = "약국소개 페이지"
        

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
    

