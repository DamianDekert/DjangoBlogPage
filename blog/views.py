from django.shortcuts import render, get_object_or_404
from datetime import date
from django.views.generic import ListView, DetailView
from django.views import View
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Author, Post, Tag
from .forms import CommentForm

all_posts = Post.objects.all()


class StartingPage(ListView):
    template_name = 'blog/index.html'
    model = Post
    context_object_name = 'posts'
    ordering = ["-date"]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        data = queryset[:3]
        return data
    

class AllPosts(ListView):
    template_name = "blog/all-posts.html"
    model = Post
    ordering = ["-date"]
    context_object_name = 'posts'


class PostDetail(View):

    def get(self, requests, slug):
        post = Post.objects.get(slug=slug)
        context = {
            'post': post,
            'post_tags': post.tag.all(),
            'comment_form' : CommentForm(),
            'comments' : post.comments.all().order_by('-id')
        }
        return render(requests, 'blog/post-detail.html', context)

    def post(self, requests, slug):
        comment_form = CommentForm(requests.POST)
        post = Post.objects.get(slug=slug)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()

            return HttpResponseRedirect(reverse('post-detail-page', args =[slug]))
        context = {
            'post': post,
            'post_tags': post.tag.all(),
            'comment_form' : comment_form,
            'comments' : post.comments.all().order_by('-id')
        }
        return render(requests, 'blog/post-detail.html', context)

class ReadLaterView(View):

    def post(self, request):
        stored_post = request.session.get('stored-post')

        if stored_post is None:
            stored_post = []