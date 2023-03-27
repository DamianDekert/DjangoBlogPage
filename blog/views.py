from django.shortcuts import render, get_object_or_404
from datetime import date
from django.views.generic import ListView, DetailView

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


def post_detail(request, slug):
    ident_post = get_object_or_404(Post, slug = slug)
    return render(request, 'blog/post-detail.html',{
        'post': ident_post
    })

class PostDetail(DetailView):
    template_name = 'blog/post-detail.html'
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_tags'] = self.object.tag.all()
        context['comment_form'] = CommentForm()
        return context
