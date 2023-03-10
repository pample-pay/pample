from rest_framework import serializers

class DsSerializer(serializers.Serializer):
    drugstore_name = serializers.CharField(max_length=256)
    drugstore_zipcode = serializers.IntegerField()
    drugstore_address = serializers.CharField(max_length=256)
    drugstore_open = serializers.CharField(max_length=256)
    drugstore_lng = serializers.FloatField()
    drugstore_lat = serializers.FloatField()
    drugstore_associate = serializers.IntegerField
    distance = serializers.FloatField()

