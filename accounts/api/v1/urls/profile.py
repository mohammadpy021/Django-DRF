from django.urls import path
from accounts.api.v1.views import (
    UserListView,
    ProfileAPIView,
)


urlpatterns = [
    # users list
    path("users/", UserListView.as_view(), name="user-list"),
    # current user detail + update
    path("profile/", ProfileAPIView.as_view(), name="profile-detail"),
]
