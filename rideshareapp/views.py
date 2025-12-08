from django.shortcuts import redirect
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden
from posts.models import Post
from django.contrib import messages
from .forms import CIOForm
from .models import CIO, CIOPlaceholderMember
from django.shortcuts import render, redirect, get_object_or_404


# SHERRIFF: very basic index page created
def index(request):
    if request.user.is_authenticated:
        #gets posts in order
        posts = Post.objects.all().order_by('-created_at')
        cios = CIO.objects.all().order_by('-id')

        #filter the posts if need to filter
        start = request.GET.get("start")
        end = request.GET.get("end")
        date = request.GET.get("date")

        if start:
            posts = posts.filter(start_location__icontains=start)

        if end:
            posts = posts.filter(end_location__icontains=end)

        #asked chat to debug the date filtering on 12/8/25, needed parse_date so that string is converted to date object
        if date:
            parsed_date = parse_date(date)
            if parsed_date:
                posts = posts.filter(departure_time__date=parsed_date)

        #asked chat for this line on 10/15/25
        #prompt how do i change this to not redirect to accounts/login
        return render(request, "rideshareapp/home.html", {"user": request.user, "posts":posts, "cios":cios,})
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
    if not request.user.is_authenticated:
        return redirect('/accounts/login')

    # Get CIO id from ?cio_id= in the query string
    cio_id = request.GET.get("cio_id")

    if not cio_id:
        return render(request, "rideshareapp/cio_dashboard.html", {"cio": None})

    cio = get_object_or_404(CIO, id=cio_id)

    # Placeholder members for this CIO
    placeholder_members = cio.placeholder_members.all()  # relies on related_name in model
    # real_members = cio.members.all()

    context = {
        "cio": cio,
        "placeholder_members": placeholder_members,
        # "real_members": real_members
    }

    return render(request, "rideshareapp/cio_dashboard.html", context)
