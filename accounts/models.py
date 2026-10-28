from django.conf import settings
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True, help_text="Profile picture")
    bio = models.TextField(blank=True, help_text="A short bio")
    link = models.URLField(blank=True, help_text="Paste a link here, e.g. your website or shop")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"@{self.user.username}"


class Subscription(models.Model):
    """Bookora membership: $5/month, first month $2.50 (50% off).

    Payment is NOT taken yet — the provider (Polo) is to be connected
    later. Until then a subscription is recorded as 'pending_payment'.
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="subscription")
    is_first_month = models.BooleanField(default=True)
    status = models.CharField(
        max_length=20,
        choices=[("pending_payment", "Pending payment"), ("active", "Active"), ("cancelled", "Cancelled")],
        default="pending_payment",
    )
    started_at = models.DateTimeField(auto_now_add=True)

    @property
    def current_price(self):
        if self.is_first_month:
            return settings.BOOKORA_FIRST_MONTH_PRICE
        return settings.BOOKORA_MONTHLY_PRICE

    def __str__(self):
        return f"{self.user.username} — {self.status} (${self.current_price})"
