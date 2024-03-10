from django.shortcuts import get_object_or_404
from rest_framework import generics, status, views
from rest_framework.response import Response
# from accounts.models import User
from django.contrib.auth import get_user_model
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import  IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail, EmailMessage
# from mail_templated import send_mail
import jwt
from jwt.exceptions import  ExpiredSignatureError, InvalidTokenError
from django.conf import settings
from accounts.api.v1.serializers.accounts import EmailVerificationResendSerializer
from accounts.api.v1.utils import EmailThread
from .serializers import (ChangePasswordSerializer, CustomAuthTokenSerializer,
                           RegistrationSerializer,
                           UesrSerializer,
                        #   CustomJWTTokenObtainPairSerializer,
                          CustomTokenObtainPairSerializer
                          )
# from .tasks import email_send

class UserListView(generics.ListAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = UesrSerializer
    queryset = get_user_model().objects.all()

class CurrentUserDetailView(generics.RetrieveUpdateAPIView):
    ''' details of current logged in user''' #(first way)
    permission_classes = [IsAuthenticated]
    serializer_class = UesrSerializer
    http_method_names = ["get", "patch"] #remove put(update)

    def get_object(self):
        ''' important:
             we put this here because we don't want to detemine the user pk in the url,
             so we won't get Lookup Field Error anymore'''
        return self.request.user
# class CurrentUserDetailView(generics.GenericAPIView):
#     ''' details of current logged in user(second way)'''
#     permission_classes = [IsAuthenticated]
#     def get(self, request, *args, **kwargs):    
#         return Response({
#             'user_id': request.user.pk,
#             'email': request.user.email,
#             'username': request.user.username,
#             'full_name': request.user.first_name + " " + request.user.last_name
#         })

class RegistrationView(generics.GenericAPIView):
    serializer_class = RegistrationSerializer
    queryset = get_user_model().objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            self.email = serializer.validated_data['email']
            user_obj = serializer.save()
            token  = self.get_tokens_for_user(user_obj)
            mail = EmailMessage("Subject here", f"{token}", "from@gmail.com",[self.email])        
            EmailThread(mail).start()
            return Response({'email': self.email }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

class CustomAuthToken(ObtainAuthToken):
    serializer_class = CustomAuthTokenSerializer 
    ''' custom response to show extra fields when user logged in'''
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email,
            'username': user.username or user.first_name + " " + user.last_name
        })

class LogoutToken(views.APIView):
    ''' custom logout token'''
    #we can also use generics.GenericAPIView but views.APIView is better here
    #because we won't get an "AssertionError" for not having a serializer
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs): 
        try:
            request.user.auth_token.delete()
        except :
            return Response({"detail": ("no token has been setted for the user yet")},
                status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT) 
    
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class ChangePasswordView(generics.GenericAPIView):
    """
    An endpoint for changing password.
    """
    #if this be 'generic.UpdateAPIView' , both 'patch' and 'update' will be in the endpoints too,
    # which we don't want the 'patch'
    # or we can use " http_method_names = ['put'] "
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer

    
    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return  Response({'message': 'Password updated successfully'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 

class EmailVerificationView(views.APIView):
    def get(self, request, token, *args, **kwargs):
        try:
            token   = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"]) #'token' is defiend in the url 
        except ExpiredSignatureError:
            return Response("token has been expired", status=status.HTTP_400_BAD_REQUEST)
        except InvalidTokenError:
            return Response("token is not valid", status=status.HTTP_400_BAD_REQUEST)
        user_id = token.get("user_id") # 'user_id" is a field inside the  decoded token
        user = get_user_model().objects.get(id=user_id)
        if user.is_verified:
            return Response("your account is already verified", status=status.HTTP_200_OK)
        user.is_verified = True
        user.save()
        return Response("your account has been verified successfully", status=status.HTTP_200_OK)

class EmailVerificationResendView(generics.GenericAPIView):

    serializer_class = EmailVerificationResendSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        user_obj = serializer.validated_data["user"]
        self.email = serializer.validated_data["email"]
        if user_obj.is_verified:# "is_verified" is a custom validation defiend in custom user model
            return Response({"detail": "Your account is already verified"}, status = status.HTTP_400_BAD_REQUEST)
        
        token  = self.get_tokens_for_user(user_obj)
        # email_send.delay("Subject here", f"{token}", [self.email])#Celery
        
        mail = EmailMessage("Subject here", f"{token}", "from@gmail.com",[self.email])
        EmailThread(mail).start() #thread
        return Response({"detail": "email has been sent"}, status = status.HTTP_200_OK)

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)