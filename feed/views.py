from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PostForm, ShortVideoForm, VideoCommentForm
from .models import Post, ShortVideo, VideoLike


def home(request):
    # Combined feed: posts + short videos, newest first by page section.
    return render(request, "feed/home.html", {
        "posts": Post.objects.select_related("author")[:20],
        "videos": ShortVideo.objects.select_related("author")[:20],
    })


def video_feed(request):
    """Scrollable short-video feed — one video per screen, swipe/scroll down."""
    videos = ShortVideo.objects.select_related("author").prefetch_related("likes", "comments")
    liked_ids = set()
    if request.user.is_authenticated:
        liked_ids = set(VideoLike.objects.filter(user=request.user).values_list("video_id", flat=True))
    return render(request, "feed/video_feed.html", {
        "videos": videos,
        "liked_ids": liked_ids,
    })


def video_detail(request, pk):
    video = get_object_or_404(ShortVideo.objects.select_related("author"), pk=pk)
    if request.method == "POST" and request.user.is_authenticated:
        form = VideoCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.video = video
            comment.save()
            messages.success(request, "Comment posted.")
            return redirect("video_detail", pk=video.pk)
    else:
        form = VideoCommentForm()
    return render(request, "feed/video_detail.html", {
        "video": video,
        "comments": video.comments.select_related("user"),
        "form": form,
        "is_liked": video.is_liked_by(request.user),
    })


@login_required
def video_like(request, pk):
    video = get_object_or_404(ShortVideo, pk=pk)
    like, created = VideoLike.objects.get_or_create(user=request.user, video=video)
    if not created:
        like.delete()
        messages.info(request, "Like removed.")
    else:
        messages.success(request, "Liked.")
    next_url = request.POST.get("next") or request.GET.get("next") or "video_feed"
    if next_url.startswith("/"):
        return redirect(next_url)
    return redirect(next_url)


@login_required
def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, "Posted to your Bookora profile.")
            return redirect("profile", username=request.user.username)
    else:
        form = PostForm()
    return render(request, "feed/post_create.html", {"form": form})


@login_required
def video_upload(request):
    if request.method == "POST":
        form = ShortVideoForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save(commit=False)
            video.author = request.user
            video.save()
            messages.success(request, "Short video uploaded.")
            return redirect("video_feed")
    else:
        form = ShortVideoForm()
    return render(request, "feed/video_upload.html", {"form": form})
