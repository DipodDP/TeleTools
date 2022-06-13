from pyrogram.raw.functions import messages

from app_init import app_init

app = app_init()

with app:
    m = app.invoke(messages.GetAllChats(except_ids=[]))
    with open("Chats.txt", 'w', encoding='utf-8') as f:
        for chat in m.chats:
            # Getting chat ID
            chat_id = str(chat.id)
            # Getting chat title
            chat_title = chat.title
            chat_username = chat.username if 'username' in repr(chat) else 'no user'
            part_count = str(chat.participants_count) if 'participants_count' in repr(chat) else '?'
            no_fwd = 'yes' if chat.noforwards else 'no'

            f.writelines(f"ID: {chat_id}, CHAT: {chat_title}, {chat_username} >> "
                         f"(PARTICIPANTS: {part_count}), NO_FWD: {no_fwd}\n")
            print(f"ID: {chat_id}, CHAT: {chat_title}, {chat_username} >> "
                  f"(PARTICIPANTS: {part_count}), NO_FWD: {no_fwd}")
