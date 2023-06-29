from rest_framework import serializers

class DsSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    
    drugstore_name = serializers.CharField(max_length=256)
    drugstore_areacode = serializers.IntegerField()
    drugstore_citycode = serializers.IntegerField()

    drugstore_zipcode = serializers.IntegerField()
    drugstore_address = serializers.CharField(max_length=256)
    drugstore_hp = serializers.CharField(max_length=256)
    drugstore_open = serializers.CharField(max_length=256)

    drugstore_lng = serializers.FloatField()
    drugstore_lat = serializers.FloatField()

    drugstore_associate = serializers.IntegerField
    
    distance = serializers.FloatField()

