from django.shortcuts import render
from django.views import generic
from blog.models import Articles
from django.contrib.auth.mixins import LoginRequiredMixin


class ArticleListView(generic.ListView):
    model = Articles


class ArticleDetailView(LoginRequiredMixin, generic.DetailView):
    model = Articles
