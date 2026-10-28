from django.conf import settings
from django.db import models


class Ebook(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="ebooks")
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    cover = models.ImageField(upload_to="ebook_covers/", blank=True, null=True)
    file = models.FileField(upload_to="ebooks/")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class Purchase(models.Model):
    """A record of a sale. Payment itself is a placeholder until
    the payment provider (Polo) is connected — see views.checkout()."""
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="purchases")
    ebook = models.ForeignKey(Ebook, on_delete=models.CASCADE, related_name="purchases")
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=[("pending_payment", "Pending payment"), ("paid", "Paid")],
        default="pending_payment",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["buyer", "ebook"]

    def __str__(self):
        return f"{self.buyer.username} bought {self.ebook.title}"
