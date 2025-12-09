from django.contrib import messages
from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post
from .forms import PostForm

@login_required
def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  
            post.save()
            #send back to home page
            return redirect('index')  
    else:
        form = PostForm()
    
    return render(request, 'posts/post_forms.html', {'form': form})

@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    # Only the creator or moderators may edit
    if request.user != post.author and not request.user.groups.filter(name='Moderator').exists():
        messages.error(request, "You do not have permission to edit this post.")
        return redirect('index')

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            # Currently always sends back to home page, which isn't ideal for admins
            return redirect('index')
    else:
        form = PostForm(instance=post)

    return render(request, 'posts/post_forms.html', {'form': form, 'post': post})

@login_required
def post_delete(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    # Only the creator or moderators may delete
    if request.user != post.author and not request.user.groups.filter(name='Moderator').exists():
        messages.error(request, "You do not have permission to delete this post.")
        return redirect('index')

    # Should probably have a way to delete the image from S3... hmm...
    post.delete()
    messages.success(request, "Post deleted successfully.")
    return redirect('index')
