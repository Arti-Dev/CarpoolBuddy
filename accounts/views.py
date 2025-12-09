from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect
from .forms import UserUpdateForm, ProfileUpdateForm
from posts.models import Post


@login_required
def profile(request, user_id):
    if user_id is None: # Viewing own profile
        profile_user = request.user
    else:
        profile_user = get_object_or_404(User, pk=user_id)

    # Get profile object


    #add posts so that a users posts can be seen on profile page
    posts = Post.objects.filter(author=profile_user).order_by('-created_at')
    return render(request, 'account/profile.html', {"profile_user":profile_user, "posts":posts})

@login_required
def profile_self(request):
    return profile(request, request.user.id)

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
    return render(request, "account/profileedit.html", {"user_update_form": user_update_form, "profile_form": profile_form})