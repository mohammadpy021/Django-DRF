from django.urls import path
from accounts.api.v1.views import (UserListView,
                                CurrentUserDetailView,)


urlpatterns = [
    #users list
    path("users/",   UserListView.as_view(),   name='user-list'),
    #current user detail + update
    path("profile/", CurrentUserDetailView.as_view(), name='user-detail'),
]
