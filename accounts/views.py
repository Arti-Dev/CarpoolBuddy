from django.contrib.auth.models import User
from django.http import HttpResponseForbidden, HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect
from .forms import UserUpdateForm, ProfileUpdateForm
from posts.models import Post
from django.contrib.auth import logout
from django.contrib.messages import get_messages



@login_required
def profile(request, user_id):
    if user_id is None: # Viewing own profile
        profile_user = request.user
    else:
        profile_user = get_object_or_404(User, pk=user_id)

    if request.user.groups.filter(name='Moderator').exists():
        is_moderator = True
    else:
        is_moderator = False


    #add posts so that a users posts can be seen on profile page
    posts = Post.objects.filter(author=profile_user).order_by('-created_at')
    return render(request, 'account/profile.html', {"profile_user":profile_user,
                                                    "posts":posts,
                                                    "is_moderator": is_moderator})

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


@login_required
def ban_user(request):
    # Permission check
    # Maybe I shouldn't hardcode Moderator. Oh well.
    if not request.user.groups.filter(name='Moderator').exists():
        return HttpResponseForbidden("You don't have permission!")

    if request.method != "POST":
        return HttpResponseBadRequest("Invalid request")

    user_id = request.POST.get("user_id", "").strip()
    action = request.POST.get("action", "").strip()

    # Prevent a moderator from banning themselves
    if str(request.user.id) == user_id:
        messages.error(request, "Yeah, don't ban yourself.")
        return redirect("accounts:profile", user_id=request.user.id)

    target_user = get_object_or_404(User, id=user_id)

    if action == "ban":
        target_user.is_active = False
        target_user.save()
        messages.success(request, f"User {target_user.username} has been banned.")
        return redirect("accounts:profile", user_id=target_user.id)
    elif action == "unban":
        target_user.is_active = True
        target_user.save()
        messages.success(request, f"User {target_user.username} has been unbanned.")
        return redirect("accounts:profile", user_id=target_user.id)
    else:
        messages.error(request, "Invalid action.")
        return redirect("accounts:profile", user_id=target_user.id)
    
#asked chatgpt for a delete account method on 12/9/25, i modified it to redirect to the pages i want
@login_required
def delete_account(request):
    if request.method != "POST":
        return HttpResponseBadRequest("Invalid request")

    user = request.user

    messages.success(request, "Your account has been permanently deleted.")

    #clears the message so "your account has been deleted" isnt still shown if you log in again
    storage = get_messages(request)
    for _ in storage:
        pass  # just iterating clears them

    #log out the user before deleting
    logout(request)
    user.delete()
    return redirect("/") 