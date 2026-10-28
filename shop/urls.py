from django.urls import path

from . import views

urlpatterns = [
    path("ebooks/", views.ebook_list, name="ebook_list"),
    path("ebooks/upload/", views.ebook_upload, name="ebook_upload"),
    path("ebooks/<int:pk>/", views.ebook_detail, name="ebook_detail"),
    path("ebooks/<int:pk>/buy/", views.checkout, name="checkout"),
    path("ebooks/<int:pk>/download/", views.ebook_download, name="ebook_download"),
    path("library/", views.my_library, name="my_library"),
]
