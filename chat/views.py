import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest, JsonResponse, HttpResponseForbidden, Http404
from django.shortcuts import render, get_object_or_404

from accounts.models import Profile
from chat.models import ChatRoom, ChatAccess
from project.storage_backend import ChatStorage


# Create your views here.

@login_required
def index(request):
    return render(request, "chat/index.html")

@login_required
def room_view(request, room_id):
    try:
        room_id = int(room_id)
    except ValueError:
        raise Http404("Invalid room ID")
    room = get_object_or_404(ChatRoom, id=room_id)

    user_profile = request.user.profile
    has_access = ChatAccess.objects.filter(user=user_profile, room=room).exists()
    if not has_access:
        return HttpResponseForbidden("You do not have access to this room.")

    messages = load_messages_from_s3(room_id)

    return render(request, "chat/room.html",
                  {"room_id": room.id,
                   "room_title": room.title,
                   "messages": messages})
@login_required
def start_chat(request):
    if request.method != "POST":
        return HttpResponseBadRequest("Invalid request")

    target_id = request.POST.get("computing_id", "").strip()
    target_profile = Profile.objects.get(computing_id=target_id)

    user_profile = request.user.profile

    existing_rooms = (ChatRoom.objects.filter(
        chataccess__user=user_profile
    ).filter(
        chataccess__user=target_profile
    ).filter(
        dm=True
    ).distinct())

    if existing_rooms.exists():
        room = existing_rooms.first()
    else:
        title = f"Conversation between {target_profile.get_display_name()} and {user_profile.get_display_name()}"
        room = ChatRoom.objects.create(title=title, dm=True)
        ChatAccess.objects.create(user=user_profile, room=room)
        ChatAccess.objects.create(user=target_profile, room=room)

    return JsonResponse({"room_id": room.id})

@login_required()
def start_group_chat(request):
    if request.method != "POST":
        return HttpResponseBadRequest("Invalid request")
    # caution - different loading method than start_chat!
    data = json.loads(request.body)
    computing_ids = data.get("computing_ids", [])
    failed_ids = []
    target_profiles = [request.user.profile]
    for id in computing_ids:
        try:
            target_profile = Profile.objects.get(computing_id=id)
            target_profiles.append(target_profile)
        except Profile.DoesNotExist:
            failed_ids.append(id)
            continue

    title = "Group Chat: " + ", ".join([p.user.profile.get_display_name() for p in target_profiles])
    room = ChatRoom.objects.create(title=title, dm=False)
    for profile in target_profiles:
        ChatAccess.objects.create(user=profile, room=room)
    return JsonResponse({"room_id": room.id, "failed_ids": failed_ids})

def validate_other_user(request):
    computing_id = request.POST.get("computing_id", "").strip()
    current_user_id = request.user.profile.computing_id

    if computing_id == current_user_id:
        return JsonResponse({"valid": False, "error": "That's you, silly!"}, status=400)
    if not computing_id:
        return JsonResponse({"valid": False, "error": "No computing ID provided"}, status=400)

    exists = Profile.objects.filter(computing_id=computing_id).exists()
    if exists:
        return JsonResponse({"valid": True})
    else:
        return JsonResponse({"valid": False, "error": f"Could not find a user by computing id {computing_id}"}, status=400)

def load_messages_from_s3(room: int):
    storage = ChatStorage()
    files = storage.listdir(str(room))[1]

    messages = []
    for file in files:
        content = storage.open(f"{str(room)}/{file}").read()
        messages.append(json.loads(content))

    return sorted(messages, key=lambda x: x["timestamp"])