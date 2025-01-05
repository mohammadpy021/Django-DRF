from rest_framework.test import APIClient
from django.urls import reverse
from django.contrib.auth import get_user_model
import pytest

@pytest.fixture()
def api_cielnt():
    client =  APIClient()
    return client

@pytest.fixture()
def common_user():
    user = get_user_model().objects.create_user(email="adminTest@test.com", password="Mm@123456", is_verified=True)
    return user

@pytest.mark.django_db(True)
class Test:
    # client = APIClient()
    def test_get_articles_response_200(self, api_cielnt):

        url = reverse('blog:api-v1:article-list')
        # response = self.client.get(url)
        response = api_cielnt.get(url)
        assert response.status_code == 200

    def test_create_article_response_401_unauthorized(self, api_cielnt):
        url = reverse('blog:api-v1:article-list')
        data = {"title":"this is title",
                "slug":"this-is-slug",
                "status":True,
                }
        response = api_cielnt.post(url, data=data)
        assert response.status_code == 401

    def test_create_article_response_201(self, api_cielnt, common_user):
        url = reverse('blog:api-v1:article-list')
        data = {"title":"this is title",
                "slug":"this-is-slug",
                "status":True,
                }
        api_cielnt.force_authenticate(user= common_user)
        response = api_cielnt.post(url, data=data)
        assert response.status_code == 201
        assert response.data['author'] == common_user.email

    def test_create_article_invalid_data_response_400(self, api_cielnt, common_user):
        url = reverse('blog:api-v1:article-list')
        data = {}
        api_cielnt.force_authenticate(user= common_user)
        response = api_cielnt.post(url, data=data)
        assert response.status_code == 400