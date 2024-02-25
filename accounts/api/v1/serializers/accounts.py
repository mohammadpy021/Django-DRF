from rest_framework import serializers
# from accounts.models import User
from django.contrib.auth import get_user_model
from django.core import exceptions
import django.contrib.auth.password_validation as validators
from django.core.mail import  EmailMessage
from rest_framework.response import Response
from rest_framework import status

from accounts.api.v1.utils import EmailThread


class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(max_length=255, write_only=True)

    class Meta:
        model = get_user_model()
        fields = ['username', 'email' , 'password', 'password2']

    def validate(self, data):
        if data.get('password') != data.get('password2') :
            raise serializers.ValidationError({"password": "passwords are not match"})
        
        try:
            ''' check the complexity of the password'''
            validators.validate_password(data.get('password'))
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})
        
        return super().validate(data)
    
    def create(self, validated_data):
        validated_data.pop("password2")
        user =  get_user_model().objects.create_user(**validated_data)
        # Token.objects.get_or_create(user=user)
        return user
    

    def to_representation(self, instance):
        """ hide passwords from <list display> """
        fields =   super().to_representation(instance)
        fields.pop('password', None)
        # fields.pop('password2', None)
        return fields

    # def get_fields(self):
        ''' hide password from <input fields> in the bottom'''
        # fields = super().get_fields()  
        # fields["password"].read_only = True
        # return fields
    
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    new_password2 = serializers.CharField(required=True)

    def validate(self, data):
        if data.get('new_password') != data.get('new_password2') :
            raise serializers.ValidationError({"new_password": "passwords are not match"})
        try:
            ''' check the complexity of the password'''
            validators.validate_password(data.get('new_password'))
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({"new_password": list(e.messages)})
        
        return super().validate(data)
    
class EmailVerificationResendSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    def validate(self, attrs):
        try:
            user_obj = get_user_model().objects.get(email=attrs.get('email'))
        except:
            raise serializers.ValidationError({"detail" : "user does not exist."})
        attrs["user"] = user_obj
        return super().validate(attrs)