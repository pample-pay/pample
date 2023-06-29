from .models import User, NormalUser, Pharmacist, ParmStaff
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'user_name', 'user_type']

    def create(self, validated_data):
        user = User.objects.create_user(
            user_id = validated_data['user_id'],
            password = validated_data['password']
        )
        return user
    
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'password', 'user_type']

    def create(self, validated_data):
        user = User.objects.create_user(
            user_id = validated_data['user_id'],
            password = validated_data['password'],
            user_type = validated_data['user_type']
        )

        if user.user_type == "2":
            NormalUser.objects.create(
                user = user
            )
        elif user.user_type == "3":
            Pharmacist.objects.create(
                user = user
            )
        elif user.user_type == "4":
            ParmStaff.objects.create(
                user = user
            )

        return user