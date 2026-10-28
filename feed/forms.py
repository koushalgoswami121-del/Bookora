from django import forms

from .models import Post, ShortVideo, VideoComment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["text", "image"]
        widgets = {"text": forms.Textarea(attrs={"rows": 3, "placeholder": "Post something on your Bookora profile..."})}


class ShortVideoForm(forms.ModelForm):
    class Meta:
        model = ShortVideo
        fields = ["caption", "video"]


class VideoCommentForm(forms.ModelForm):
    class Meta:
        model = VideoComment
        fields = ["text"]
        widgets = {"text": forms.Textarea(attrs={"rows": 2, "placeholder": "Add a comment..."})}
