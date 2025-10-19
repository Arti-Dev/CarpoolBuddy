from django.shortcuts import redirect
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden


# SHERRIFF: very basic index page created
def index(request):
    if request.user.is_authenticated:
        #asked chat for this line on 10/15/25
        #prompt how do i change this to not redirect to accounts/login
        return render(request, "rideshareapp/home.html", {"user": request.user})
    else:
        return redirect('/accounts/login')

def moderator(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')
    if request.user.groups.filter(name='Moderator').exists():
        return render(request, 'rideshareapp/moderator.html')
    else:
        return HttpResponseForbidden("You don't have permission!")