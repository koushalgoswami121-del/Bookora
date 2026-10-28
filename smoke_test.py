"""Smoke test for Bookora — run with: .venv/bin/python smoke_test.py"""
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bookora.settings")
django.setup()

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client

c = Client()
for url in ["/", "/videos/", "/ebooks/", "/pricing/", "/signup/", "/login/"]:
    r = c.get(url)
    print(url, r.status_code)
    assert r.status_code == 200, url

# Sign up, then check profile pages
r = c.post("/signup/", {"username": "testauthor", "email": "a@example.com", "password1": "TestPass12345", "password2": "TestPass12345"})
print("signup POST", r.status_code)
assert r.status_code in (200, 302)

r = c.get("/@testauthor/")
print("profile", r.status_code)
assert r.status_code == 200

# Edit profile with pic, bio, link
from PIL import Image
import io
buf = io.BytesIO()
Image.new("RGB", (10, 10), "red").save(buf, format="PNG")
buf.seek(0)
r = c.post("/profile/edit/", {
    "bio": "I write short travel books.",
    "link": "https://example.com/my-book",
    "avatar": SimpleUploadedFile("pic.png", buf.read(), content_type="image/png"),
})
print("profile edit", r.status_code)
assert r.status_code in (200, 302)

# Upload an ebook and a short video and a post
r = c.post("/ebooks/upload/", {
    "title": "My First Ebook", "description": "A test book", "price": "4.99",
    "file": SimpleUploadedFile("book.pdf", b"%PDF-test", content_type="application/pdf"),
})
print("ebook upload", r.status_code)
assert r.status_code in (200, 302)

r = c.post("/videos/upload/", {
    "caption": "My first short",
    "video": SimpleUploadedFile("short.mp4", b"fake-video", content_type="video/mp4"),
})
print("video upload", r.status_code)
assert r.status_code in (200, 302)

r = c.post("/post/", {"text": "Hello Bookora!"})
print("post", r.status_code)
assert r.status_code in (200, 302)

for url in ["/", "/videos/", "/ebooks/", "/@testauthor/", "/pricing/"]:
    r = c.get(url)
    print("after content", url, r.status_code)
    assert r.status_code == 200

# Like and comment on the uploaded video (id 1, first created)
from feed.models import ShortVideo
video = ShortVideo.objects.first()
assert video is not None
r = c.post(f"/videos/{video.pk}/like/", {"next": "/videos/"})
print("video like", r.status_code)
assert r.status_code in (200, 302)
video.refresh_from_db()
assert video.like_count == 1, video.like_count

r = c.post(f"/videos/{video.pk}/", {"text": "Great short!"})
print("video comment", r.status_code)
assert r.status_code in (200, 302)
video.refresh_from_db()
assert video.comment_count == 1, video.comment_count

r = c.get(f"/videos/{video.pk}/")
print("video detail", r.status_code, "Great short!" in r.content.decode())
assert r.status_code == 200
assert "Great short!" in r.content.decode()

# Tap like again to unlike
r = c.post(f"/videos/{video.pk}/like/", {"next": f"/videos/{video.pk}/"})
video.refresh_from_db()
assert video.like_count == 0, video.like_count
print("video unlike OK")

# Pricing math check
from django.conf import settings
assert settings.BOOKORA_FIRST_MONTH_PRICE == 2.50
assert settings.BOOKORA_MONTHLY_PRICE == 5.00
print("pricing OK: first month $2.50, then $5.00")
print("ALL SMOKE TESTS PASSED")
