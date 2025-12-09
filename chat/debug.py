from project.storage_backend import ChatStorage


def delete_all_messages(room: int):
    storage = ChatStorage()
    files = storage.listdir(str(room))[1]
    for f in files:
        storage.delete(f"{str(room)}/{f}")
    print(f"Deleted all messages in {room}")

def nuke_s3_messages():
    storage = ChatStorage()
    rooms = storage.listdir('')[0]
    for room in rooms:
        delete_all_messages(int(room))
    print("Nuked all messages in all rooms")