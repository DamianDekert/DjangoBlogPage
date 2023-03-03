from django.shortcuts import render

# blogs = {
#     'blog_post_1' : "Hello everybody! Today....",
#     'blog_post_2' : "Hey second day about....",
#     'blog_post_3' : "Hey third day about....",
#     'blog_post_4' : "Hello everybody! Today....",
#     'blog_post_5' : "Hey second day about....",
#     'blog_post_6' : "Hey third day about....",
#     'blog_post_7' : "Hello everybody! Today....",
#     'blog_post_8' : "Hey second day about....",
#     'blog_post_9' : "Hey third day about....",
#     'blog_post_10' : "Hel   lo everybody! Today....",
#     'blog_post_11' : "Hey second day about....",
#     'blog_post_12' : "Hey third day about....",
# }
# Create your views here.
def starting_page(request):
    return render(request, 'blog/index.html')

def posts(request):
    pass

def post_detail(request):
    pass