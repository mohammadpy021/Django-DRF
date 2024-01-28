from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
class Articles(models.Model):
    title= models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(max_length=255, unique=True, default='') 
    author = models.ForeignKey(get_user_model(),verbose_name=("نویسنده"),on_delete=models.CASCADE ,related_name='articles')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=("تاریخ انتشار"))
    updated_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField()
    categories = models.ManyToManyField("category",  null = True, blank = True, related_name="artilces" )

    class Meta:
        verbose_name =("مقاله")
        verbose_name_plural = ("مقاله ها ")
    def __str__(self):
        return self.title
    def get_snippet(self):
        return self.description[0:30]
    def get_absolute_api_url(self):
        return reverse("api-v1:article-detail", kwargs={"pk": self.pk})
    
class Category(models.Model):
    title= models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, default='') 
    status = models.BooleanField()


    class Meta:
        verbose_name =("دسته‌بندی")
        verbose_name_plural = ("دسته‌بندی ها ")
    def __str__(self):
        return self.title
    
