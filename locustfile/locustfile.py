from locust import HttpUser, task, between
# from django.urls import reverse

# import os, django

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
# django.setup()

class WebsiteUser(HttpUser):

    custom_host = "http://backend:8000"


    wait_time = between(1, 5)

    def on_start(self):
        # reverse("accounts:api-v1:jwt_obtain_pair"),
        response = self.client.post('/accounts/api/v1/jwt/create/', data = {
            "email": "admin@gmail.com",
            "password": "123"
            }).json()
        access_token = response.get("access", None)
        self.client.headers = {"Authorization": f"Bearer {access_token}"}

    @task
    def get_articles(self):
        # self.client.get(reverse("blog:api-v1:article-list"))
        self.client.get(f'/api/v1/articles/')
    
    @task
    def get_categories(self):
        # self.client.get(reverse("blog:api-v1:category-list"))
        self.client.get(f'/api/v1/category/')

