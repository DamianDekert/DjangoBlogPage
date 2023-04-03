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

    def is_stored_posts(self, request, post_id):
        stored_posts = request.session.get('stored-post')
        if stored_posts is not None:
            is_saved_for_later = post_id in stored_posts
        else:
            is_saved_for_later = False

        return is_saved_for_later
    
    def get(self, requests, slug):
        post = Post.objects.get(slug=slug)

        context = {
            'post': post,
            'post_tags': post.tag.all(),
            'comment_form' : CommentForm(),
            'comments' : post.comments.all().order_by('-id'),
            'saved_for_later' : self.is_stored_posts(requests, post.id)
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
            'comments' : post.comments.all().order_by('-id'),
            'saved_for_later' : self.is_stored_posts(requests, post.id)
        }
        return render(requests, 'blog/post-detail.html', context)

class ReadLaterView(View):

    def get(self, request):
        stored_post = request.session.get('stored-post')

        context = {}

        if stored_post is None or len(stored_post) == 0:
            context['posts'] = []
            context['has_posts'] = False
        else:
            posts = Post.objects.filter(id__in=stored_post)
            context['posts'] = posts
            context['has_posts'] = True
        return render(request, 'blog/stored-posts.html', context)

    def post(self, request):
        stored_post = request.session.get('stored-post')

        if stored_post is None:
            stored_post = []

        post_id = int(request.POST['post_id'])

        if post_id not in stored_post:
            stored_post.append(post_id)
        else:
            stored_post.remove(post_id)

        request.session['stored-post'] = stored_post

        return HttpResponseRedirect("/")

        