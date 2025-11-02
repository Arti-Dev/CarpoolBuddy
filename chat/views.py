from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import render

from accounts.models import Profile
from chat.models import ChatRoom, ChatAccess


# Create your views here.

def index(request):
    return render(request, "chat/index.html")

def room(request, room_name):
    return render(request, "chat/room.html", {"room_name": room_name})

def start_chat(request):
    if request.method != "POST":
        return HttpResponseBadRequest("Invalid request")

    target_id = request.POST.get("computing_id", "").strip()
    if not target_id:
        return HttpResponseBadRequest("No computing ID provided")

    try:
        target_profile = Profile.objects.get(computing_id=target_id)
    except Profile.DoesNotExist:
        return JsonResponse({"error": f"Could not find a user by computing id {target_id}"})

    user_profile = request.user.profile

    existing_rooms = ChatRoom.objects.filter(
        chataccess__user=user_profile
    ).filter(
        chataccess__user=target_profile
    ).distinct()

    if existing_rooms.exists():
        room = existing_rooms.first()
    else:
        title = f"{target_profile.user.username}{user_profile.user.username}"
        room = ChatRoom.objects.create(title=title)
        ChatAccess.objects.create(user=user_profile, room=room)
        ChatAccess.objects.create(user=target_profile, room=room)

    # todo should return room id
    return JsonResponse({"room_name": room.title})