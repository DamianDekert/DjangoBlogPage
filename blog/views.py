from django.shortcuts import render, get_object_or_404
from datetime import date
from django.views.generic import ListView, DetailView
from django.views import View
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Author, Post, Tag
from .forms import CommentForm

all_posts = Post.objects.all()

# Create your views here.
# def starting_page(request):
#     sorted_post = all_posts.order_by('-date')[:3]
#     return render(request, 'blog/index.html', {
#         'posts': sorted_post,
#     })

class StartingPage(ListView):
    template_name = 'blog/index.html'
    model = Post
    context_object_name = 'posts'
    ordering = ["-date"]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        data = queryset[:3]
        return data
    


# def posts(request):
#     all_posts_date = all_posts.order_by("-date")
#     return render(request, "blog/all-posts.html", {
#         'posts': all_posts_date,
#     })

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
