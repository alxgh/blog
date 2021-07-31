from django.contrib.auth.models import User
from rest_framework import serializers


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data["username"]
        )

        user.set_password(validated_data["password"])

        user.save()

        return user


class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']


class UpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'password']

    def update(self, instance: User, validated_data) -> User:
        if 'first_name' in validated_data:
            instance.first_name = validated_data["first_name"]
        if 'last_name' in validated_data:
            instance.last_name = validated_data["last_name"]
        if 'password' in validated_data:
            instance.set_password(validated_data["password"])
        instance.save()

        return instance