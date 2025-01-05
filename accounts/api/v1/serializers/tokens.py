from rest_framework import serializers
# from accounts.models import User
from django.contrib.auth import  authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer,  TokenObtainSerializer


class CustomAuthTokenSerializer(serializers.Serializer):
    ''' customization of  serializer of AuthTokenSerializer '''
    email = serializers.EmailField(
        label=("Email"),
        write_only=True
    )
    password = serializers.CharField(
        label=("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )
    token = serializers.CharField(
        label=("Token"),
        read_only=True
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        
        if email and password:
            user = authenticate(request=self.context.get('request'),
                                email=email, password=password) #return None for is_active=False
            
            # The authenticate call simply used to return None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            #you can use AUTHENTICATION_BACKENDS = ['django.contrib.auth.backends.AllowAllUsersModelBackend'] in settings
            if not user:
                msg = ('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
            if not user.is_verfied:
                raise serializers.ValidationError({'details':'user is not verified.'})
        else:
            msg = ('Must include "email" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
    
    
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    ''' customizes of TokenObtainPairSerializer to add more fields '''
    def validate(self, attrs):
        # username = attrs.get('username')
        # password = attrs.get('password')
        # user = authenticate(request=self.context.get('request'),username=username, password=password) 
        if not self.user.is_verfied:
            raise serializers.ValidationError({'details':'user is not verified.'})
        data = super().validate(attrs)
        data['id']       = str(self.user.id)      # we have access to the user through the parent classes
        # data['username'] = str(self.user.username) 
        data['email']    = str(self.user.email)
        return data