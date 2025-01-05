from django.urls import path
from accounts.api.v1.views import (
    RegistrationView,
    CustomAuthToken,
    LogoutToken,
    CustomTokenObtainPairView,
    ChangePasswordView,
    EmailVerificationView,
    EmailVerificationResendView,
)
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)


urlpatterns = [
    # change password
    path("change-password/", ChangePasswordView.as_view(), name="change-password"),
    # registration
    path("registration/", RegistrationView.as_view()),
    # email verification
    path("email/confirm/<str:token>/", EmailVerificationView.as_view()),
    # resend email verification
    path("email/resend/", EmailVerificationResendView.as_view()),
    # path('email/resend/', EmailVerificationView.as_view),
    # Token authentication
    path("token/login/", CustomAuthToken.as_view(), name="token-login"),
    path("token/logout/", LogoutToken.as_view(), name="token-logout"),
    # JWT
    path("jwt/create/", CustomTokenObtainPairView.as_view(), name="jwt_obtain_pair"),
    path("jwt/refresh/", TokenRefreshView.as_view(), name="jwt_refresh"),
    path("jwt/verify/", TokenVerifyView.as_view(), name="jwt_verify"),
]
