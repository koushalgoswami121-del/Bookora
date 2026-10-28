from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("videos/", views.video_feed, name="video_feed"),
    path("videos/upload/", views.video_upload, name="video_upload"),
    path("videos/<int:pk>/", views.video_detail, name="video_detail"),
    path("videos/<int:pk>/like/", views.video_like, name="video_like"),
    path("post/", views.post_create, name="post_create"),
]
