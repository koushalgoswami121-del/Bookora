from django.contrib import admin

from .models import Post, ShortVideo, VideoComment, VideoLike

admin.site.register(Post)
admin.site.register(ShortVideo)
admin.site.register(VideoLike)
admin.site.register(VideoComment)
