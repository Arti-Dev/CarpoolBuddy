from django.shortcuts import redirect
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden
from posts.models import Post
from django.contrib import messages
from .forms import CIOForm
from .models import CIO, CIOPlaceholderMember


# SHERRIFF: very basic index page created
def index(request):
    if request.user.is_authenticated:
        #gets posts in order
        posts = Post.objects.all().order_by('-created_at')
        #asked chat for this line on 10/15/25
        #prompt how do i change this to not redirect to accounts/login
        return render(request, "rideshareapp/home.html", {"user": request.user, "posts":posts})
    else:
        return redirect('/accounts/login')

def moderator(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')
    if request.user.groups.filter(name='Moderator').exists():
        return render(request, 'rideshareapp/moderator.html')
    else:
        return HttpResponseForbidden("You don't have permission!")
    
def admin_dashboard(request):
    return render(request, "rideshareapp/admin_dashboard.html")

def admin_add_user(request):
    return render(request, "rideshareapp/admin_add_user.html")

def admin_my_groups(request):
    return render(request, "rideshareapp/admin_my_groups.html")

def admin_create_cio(request):
    if request.method == 'POST':
        form = CIOForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/rideshareapp/admin-dashboard/?created=1')
    else:
        form = CIOForm()

    return render(request, 'rideshareapp/admin_create_cio.html', {'form': form})
def cio_dashboard(request):
    #if not request.user.is_authenticated:
    #    return redirect('/accounts/login')
    cioName= "Placeholder name"
    return render(request, "rideshareapp/cio_dashboard.html", { "cio_name": cioName })
