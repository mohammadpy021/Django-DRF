from rest_framework import serializers

# from accounts.models import User
from django.contrib.auth import get_user_model
from accounts.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = Profile
        # fields = ['user'] # 'user' will return the email too
        fields = ["id", "email", "first_name", "last_name", "image", "description"]
