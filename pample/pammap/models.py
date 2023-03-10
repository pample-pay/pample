from .choices import *
from django.db import models


class DRUGSTORE(models.Model):
    drugstore_name = models.CharField(max_length=256, verbose_name="약국명")
    drugstore_zipcode = models.IntegerField(verbose_name="우편번호")
    drugstore_address = models.CharField(max_length=256, verbose_name="주소")
    drugstore_open = models.CharField(max_length=256, verbose_name="개점일")

    drugstore_lng = models.FloatField(verbose_name="경도", default='None')
    drugstore_lat = models.FloatField(verbose_name="위도", default='None')

    drugstore_associate = models.IntegerField(choices=ASSOCIATE_CHOICES,
                                              default = '0',
                                              verbose_name="제휴여부")

    def __str__(self):
        return str(self.drugstore_name)
    
    class Meta:
        db_table = "DRUGSTORE_TB"
        verbose_name = "약국정보"
        verbose_name_plural = "약국정보"
        

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)