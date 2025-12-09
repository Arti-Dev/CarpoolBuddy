from project.storage_backend import ChatStorage


def delete_all_messages(room: int):
    storage = ChatStorage()
    files = storage.listdir(room)[1]
    for f in files:
        storage.delete(f"{str(room)}/{f}")
    print(f"Deleted all messages in {room}")