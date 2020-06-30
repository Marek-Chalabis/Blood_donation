from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import ProfileUpdateForm, UserRegisterForm, UserUpdateForm


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            secret_word = form.cleaned_data.get("secret_word")
            if secret_word.lower() == "pickle ricky":
                form.save()
                username = form.cleaned_data.get("username")
                messages.success(
                    request,
                    f"{username} Your account has been created! You are able to Log In",
                )
                return redirect("login")
            else:
                messages.warning(
                    request,
                    "You passed wrong secret word, only medical employees can register",
                )
                return redirect("main")
    else:
        form = UserRegisterForm()
    return render(request, "users/register.html", {"form": form})


@login_required
def profile(request):
    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile
        )
        if user_form.is_valid() and profile_form.is_valid():
            profile_form.save()
            user_form.save()
            messages.success(request, f"Your account has been updated")
            return redirect("profile")
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {"user_form": user_form, "profile_form": profile_form}
    return render(request, "users/profile.html", context)
