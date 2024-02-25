from django.urls import path, include
from rest_framework import routers
from blog.api.v1.views import ArticlesViewSet

router = routers.SimpleRouter()
router.register(r'', ArticlesViewSet , basename='articles-basename')

app_name = "accounts"


urlpatterns = [
    path("api/v1/", include('accounts.api.v1.urls') ),
    path ('', include('django.contrib.auth.urls')),
]
