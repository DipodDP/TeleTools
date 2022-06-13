import time

from pyrogram.errors import FloodWait, ChatForwardsRestricted

from app_init import app_init
from config import load_config

app = app_init()
config = load_config()

with app:
    chat_id = input("Enter channel ID")

    # async def rs_messages(app: Client, chat_id: int)
    last = False
    i = 1
    channel_id = config.channel_id

    while last < 29:

        m = app.get_messages(chat_id, i)
        if not m.empty:
            last = 1
            caption = m.caption if m.caption is not None else ''

            print(m.text.split('\n')[0] if m.text is not None else 'no text', m.caption,
                  getattr(getattr(m, "chat", None), "id", None), getattr(getattr(m, "chat", None), "title", None),
                  getattr(getattr(m, "from_user", None), "first_name", None), m.reply_to_message_id, i)

            if m.from_user is not None:
                caption = f'{caption}\nFrom:' \
                          f'{(" " + m.from_user.first_name) if m.from_user.first_name is not None else ""}' \
                          f'{(" " + m.from_user.last_name) if m.from_user.last_name is not None else ""}'

            if m.sender_chat is not None:
                m.sender_chat.has_protected_content = False
                m.sender_chat.id = channel_id
                m.sender_chat.title = f'{caption}\n{m.sender_chat.title}'

            m.chat.id = channel_id

            if m.chat.title is not None:
                caption = f'{caption}\n{m.chat.title}'
                m.chat.title = ''

            m.caption = caption
            m.chat.has_protected_content = False
            m.text = (m.text + "\n" + caption) if m.text is not None else None

            last_message = m.id
            time.sleep(1.2)

            try:
                sent = m.copy(config.channel_id)

            except FloodWait as e:
                print(e, e.value)
                time.sleep(e.value)
                i -= 1
            except ChatForwardsRestricted:
                file = app.download_media(m, in_memory=True)
                app.send_document(config.channel_id, file) if m.document is not None else None
            except Exception as e:
                print(m)
                print(e, last_message)

        else:
            last += 1
            print(i)

        i += 1

print(last_message)
