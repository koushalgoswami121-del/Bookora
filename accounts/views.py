from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ProfileForm, SignUpForm
from .models import Profile, Subscription


def logout_view(request):
    logout(request)
    return redirect("home")


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.get_or_create(user=user)
            login(request, user)
            messages.success(request, "Welcome to Bookora!")
            return redirect("profile_edit")
    else:
        form = SignUpForm()
    return render(request, "accounts/signup.html", {"form": form})


def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    profile, _ = Profile.objects.get_or_create(user=user)
    return render(request, "accounts/profile.html", {
        "profile_user": user,
        "profile": profile,
        "ebooks": user.ebooks.all(),
        "posts": user.posts.all(),
        "videos": user.short_videos.all(),
    })


@login_required
def profile_edit(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated.")
            return redirect("profile", username=request.user.username)
    else:
        form = ProfileForm(instance=profile)
    return render(request, "accounts/profile_edit.html", {"form": form})


def pricing(request):
    subscription = None
    if request.user.is_authenticated:
        subscription, _ = Subscription.objects.get_or_create(user=request.user)
    return render(request, "accounts/pricing.html", {
        "monthly": settings.BOOKORA_MONTHLY_PRICE,
        "first_month": settings.BOOKORA_FIRST_MONTH_PRICE,
        "subscription": subscription,
    })


@login_required
def subscribe(request):
    subscription, _ = Subscription.objects.get_or_create(user=request.user)
    if request.method == "POST":
        # PAYMENT HOOK — connect Polo here later.
        # Do NOT take real money in this version: record the intent
        # and show the user what they will pay once Polo is connected.
        subscription.status = "pending_payment"
        subscription.save()
        messages.info(
            request,
            f"You're on the Bookora plan at ${subscription.current_price:.2f} for this month "
            f"({'first month, 50% off' if subscription.is_first_month else 'then $5.00/month'}). "
            "Payment will be connected via Polo later — nothing has been charged yet.",
        )
        return redirect("pricing")
    return render(request, "accounts/subscribe.html", {"subscription": subscription})
