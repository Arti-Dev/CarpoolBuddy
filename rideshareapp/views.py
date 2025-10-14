from django.shortcuts import redirect
from django.shortcuts import render
from django.http import HttpResponse

# SHERRIFF: very basic index page created
def index(request):
    return redirect('/accounts/login')

def moderator(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')
    if request.user.groups.filter(name='Moderator').exists():
        return HttpResponse("Moderator")
    else:
        return HttpResponse("You don't have permission!")