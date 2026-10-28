from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404, redirect, render

from .forms import EbookForm
from .models import Ebook, Purchase


def ebook_list(request):
    return render(request, "shop/ebook_list.html", {"ebooks": Ebook.objects.all()})


def ebook_detail(request, pk):
    ebook = get_object_or_404(Ebook, pk=pk)
    owned = False
    if request.user.is_authenticated:
        owned = Purchase.objects.filter(buyer=request.user, ebook=ebook).exists()
    return render(request, "shop/ebook_detail.html", {"ebook": ebook, "owned": owned})


@login_required
def ebook_upload(request):
    if request.method == "POST":
        form = EbookForm(request.POST, request.FILES)
        if form.is_valid():
            ebook = form.save(commit=False)
            ebook.author = request.user
            ebook.save()
            messages.success(request, "Ebook listed for sale.")
            return redirect("ebook_detail", pk=ebook.pk)
    else:
        form = EbookForm()
    return render(request, "shop/ebook_upload.html", {"form": form})


@login_required
def checkout(request, pk):
    ebook = get_object_or_404(Ebook, pk=pk)
    purchase, created = Purchase.objects.get_or_create(
        buyer=request.user, ebook=ebook, defaults={"amount": ebook.price}
    )
    if request.method == "POST":
        # PAYMENT HOOK — connect Polo here later.
        # This records the sale without charging real money yet.
        messages.info(
            request,
            f"Order recorded for '{ebook.title}' at ${ebook.price:.2f}. "
            "Payment will be connected via Polo later — nothing has been charged yet. "
            "You can download it from your library once payment is live.",
        )
        return redirect("my_library")
    return render(request, "shop/checkout.html", {"ebook": ebook, "purchase": purchase})


@login_required
def my_library(request):
    return render(request, "shop/my_library.html", {"purchases": request.user.purchases.select_related("ebook")})


@login_required
def ebook_download(request, pk):
    ebook = get_object_or_404(Ebook, pk=pk)
    is_author = ebook.author == request.user
    is_buyer = Purchase.objects.filter(buyer=request.user, ebook=ebook).exists()
    if not (is_author or is_buyer):
        raise Http404("You haven't bought this ebook yet.")
    return FileResponse(ebook.file.open("rb"), as_attachment=True, filename=ebook.file.name.split("/")[-1])
