from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.urls import reverse


class Articles(models.Model):
    """
    posts for blog app
    """

    title = models.CharField(max_length=255)
    image = models.ImageField(("Image"), null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(max_length=255, unique=True, default="")
    author = models.ForeignKey(
        "accounts.profile",
        verbose_name=("نویسنده"),
        on_delete=models.CASCADE,
        related_name="articles",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=("تاریخ انتشار"))
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True)
    status = models.BooleanField(default=False)
    categories = models.ManyToManyField("category", blank=True, related_name="artilces")

    class Meta:
        verbose_name = "مقاله"
        verbose_name_plural = "مقاله ها "

    def __str__(self):
        return self.title

    def get_snippet(self):
        if self.description is not None:
            return self.description[0:30]
        return ""

    def get_absolute_api_url(self):
        """returning the relattive url"""
        return reverse("blog:api-v1:article-detail", kwargs={"pk": self.pk})


class Category(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, default="")
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name = "دسته‌بندی"
        verbose_name_plural = "دسته‌بندی ها"

    def __str__(self):
        return self.title
