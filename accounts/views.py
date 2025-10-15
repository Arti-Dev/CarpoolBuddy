from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect
from .forms import UserUpdateForm, ProfileUpdateForm

@login_required
def profile(request):
    return render(request, 'account/profile.html')
@login_required
def profile_edit(request):
    if request.method == "POST":
        user_update_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if user_update_form.is_valid() and profile_form.is_valid():
            user_update_form.save()
            profile_form.save()
            messages.success(request, "Profile updated!")
            return redirect("accounts:profile")
    else:
        user_update_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    return render(request, "account/profile_edit.html", {"user_update_form": user_update_form, "profile_form": profile_form})