from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest
from django.utils.dateparse import parse_date

from chat.models import ChatRoom
from posts.models import Post
from django.contrib import messages
from .forms import CIOForm
from .models import CIO, CIOPlaceholderMember, ReportedMessage, ReportedPost
from django.shortcuts import render, redirect, get_object_or_404
from accounts.models import Profile


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
        # asked chat how to implement photo visibility so that it checks whether or not users have acess to view photo on 12/8/25
        # gave me the following loop to add
        for p in posts:
            p.can_view_photo_user = p.can_view_photo(request.user)


        #asked chat for this line on 10/15/25
        #prompt how do i change this to not redirect to accounts/login
        return render(request, "rideshareapp/home.html", {"user": request.user, "posts":posts, "cios":cios,})
    else:
        return redirect('/accounts/login')
    
def admin_dashboard(request):
    return render(request, "rideshareapp/admin_dashboard.html")

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

def dismiss_welcome(request):
    profile = request.user.profile
    profile.onboarded = True
    profile.save()

    return redirect('index')

def report_message(request):
    if request.method != "POST":
        return HttpResponseBadRequest("Invalid request")

    message = request.POST.get("message", "").strip()
    room_id = request.POST.get("room_id", "").strip()
    reason = request.POST.get("reason", "").strip()
    message_author_computing_id = request.POST.get("message_author_computing_id", "").strip()

    # Find corresponding profile
    try:
        message_author_profile = Profile.objects.get(
            computing_id=message_author_computing_id,
        )
    except Profile.DoesNotExist:
        return HttpResponseBadRequest("Invalid message author")

    # Get the user corresponding to the profile
    message_author_user = message_author_profile.user

    if not message or not room_id:
        return HttpResponseBadRequest("Invalid report data")

    chatroom = ChatRoom.objects.get(id=room_id)
    title = chatroom.title

    ReportedMessage.objects.create(
        message=message,
        room=title,
        message_author_user=message_author_user,
        reason=reason)

    return HttpResponse("Reported message successfully")

@login_required
def review_flagged_messages(request):
    reports = ReportedMessage.objects.all()
    return render(request, "rideshareapp/review_flagged_messages.html", {"reports": reports})

def resolve_flagged_message(request):
    if request.method != "POST":
        return HttpResponseBadRequest("Invalid request")

    report_id = request.POST.get("report_id", "").strip()

    try:
        report = ReportedMessage.objects.get(id=report_id)
    except ReportedMessage.DoesNotExist:
        messages.error(request, f"Report id {report_id} does not exist.")
        return redirect('/rideshareapp/admin/review-flagged-messages/')

    report.delete()

    messages.success(request, "Reported message has been resolved.")
    return redirect('/rideshareapp/admin/review-flagged-messages/')

@login_required
def review_flagged_posts(request):
    reports = ReportedPost.objects.all()
    return render(request, "rideshareapp/review_flagged_posts.html", {"reports": reports})

def report_post(request):
    if request.method != "POST":
        return HttpResponseBadRequest("Invalid request")

    post_id = request.POST.get("post_id", "").strip()
    reason = request.POST.get("reason", "").strip()

    post = get_object_or_404(Post, id=post_id)

    ReportedPost.objects.create(
        post=post,
        reason=reason
    )
    messages.success(request, "Post reported successfully.")
    return redirect('index')

@login_required
def resolve_flagged_post(request):
    if request.method != "POST":
        return HttpResponseBadRequest("Invalid request")

    report_id = request.POST.get("report_id", "").strip()

    try:
        report = ReportedPost.objects.get(id=report_id)
    except ReportedPost.DoesNotExist:
        messages.error(request, f"Report id {report_id} does not exist.")
        return redirect('/rideshareapp/admin/review-flagged-posts/')

    report.delete()

    messages.success(request, "Reported post has been resolved.")
    return redirect('/rideshareapp/admin/review-flagged-posts/')
