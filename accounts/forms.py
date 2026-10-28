from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Profile


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["avatar", "bio", "link"]
        widgets = {
            "bio": forms.Textarea(attrs={"rows": 4, "placeholder": "Tell readers about yourself..."}),
            "link": forms.URLInput(attrs={"placeholder": "https://your-link-here"}),
        }
