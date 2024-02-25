from locust import HttpUser, task
from django.urls import reverse

import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

class HelloWorldUser(HttpUser):
    # host = "http://127.0.0.1:8000"

    def on_start(self):
        response = self.client.post(reverse("accounts:api-v1:jwt_obtain_pair"),
                        {
                        "email": "admin@gmail.com",
                        "password": "123"
                        }).json()
        access_token = response.get("access")
        self.client.headers = {"Authorization": "Bearer " + access_token}

    @task
    def post_list(self):
        self.client.get(reverse("blog:api-v1:article-list"))
    @task
    def category_list(self):
        self.client.get(reverse("blog:api-v1:category-list"))



# locust -f locustfile/locustfile.py --headless -u 10 -r 1 --host http://127.0.0.1:8000
        
