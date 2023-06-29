from db.models import DRUGSTORE_TB, DRUGSTORE_VIEW_TB
from rest_framework import serializers

# 이미지 Post 추가 serializer
class DlSerializer(serializers.ModelSerializer):
    drugstore_thumbnail = serializers.ImageField(use_url=True)

    class Meta:
        model = DRUGSTORE_VIEW_TB
        fields = ["drugstore_thumbnail", "drugstore_abstract", "drugstore_content"]

# 기본 serializer
class DlViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = DRUGSTORE_VIEW_TB
        fields = ["drugstore_thumbnail", "drugstore_abstract", "drugstore_content"]

# 상세페이지 return serializer
class DrugStoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = DRUGSTORE_TB
        fields = ["drugstore_name", "drugstore_zipcode", "drugstore_address",
                  "drugstore_hp", "drugstore_open",
                  "drugstore_lng", "drugstore_lat",
                  "drugstore_associate"]
