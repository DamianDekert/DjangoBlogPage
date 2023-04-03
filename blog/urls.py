from django.urls import path
from django.conf.urls.static import static
from django.conf import settings


from . import views


urlpatterns = [
    path('', views.StartingPage.as_view(), name='starting-page'),
    path('posts', views.AllPosts.as_view(), name='posts-page'),
    path('posts/<slug>', views.PostDetail.as_view(),
          name="post-detail-page"),#/posts/my-first-post
    path('read-later', views.ReadLaterView.as_view(), name='read-later')  
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
