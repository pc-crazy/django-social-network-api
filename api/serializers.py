from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import User, FriendRequest


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class FriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = ['id', 'from_user', 'to_user', 'status', 'created_at']


class UpdateFriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = ['status']
        extra_kwargs = {
            'status': {'required': True}
        }

    def validate_status(self, value):
        if value not in ['accepted', 'rejected']:
            raise serializers.ValidationError("Status must be 'accepted' or 'rejected'.")
        return value


class SendFriendRequestSerializer(serializers.ModelSerializer):
    to_user = serializers.CharField()

    class Meta:
        model = FriendRequest
        fields = ['to_user']


class AuthTokenSerializer(serializers.Serializer):
    email = serializers.CharField(
        write_only=True
    )
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )
    token = serializers.CharField(
        read_only=True
    )

    # def validate(self, attrs):
    #     email = attrs.get('email')
    #     password = attrs.get('password')
    #
    #     if email and password:
    #         user = authenticate(request=self.context.get('request'),
    #                             email=email, password=password)
    #
    #         # The authenticate call simply returns None for is_active=False
    #         # users. (Assuming the default ModelBackend authentication
    #         # backend.)
    #         if not user:
    #             msg = ('Unable to log in with provided credentials.')
    #             raise serializers.ValidationError(msg, code='authorization')
    #     else:
    #         msg = ('Must include "username" and "password".')
    #         raise serializers.ValidationError(msg, code='authorization')
    #
    #     attrs['user'] = user
    #     return attrs
