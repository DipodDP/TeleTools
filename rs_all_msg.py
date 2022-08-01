import time

from pyrogram.errors import FloodWait, ChatForwardsRestricted

from app_init import app_init
from config import load_config
app = app_init()


async def progress(current, total):
    print(f"{current * 100 / total:.1f}%")


async def main():

    await app.start()

    config = load_config()
    chat_id = input("Enter channel ID: ")

    # async def rs_messages(app: Client, chat_id: int)
    last = False
    i = input("Enter message id to start from: ")
    if i is None:
        i = 1
    i = int(i)

    channel_id = config.channel_id

    while last < 29:

        m = await app.get_messages(chat_id, i)
        if not m.empty:
            print(m)
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
            time.sleep(1.6)

            try:
                sent = await m.copy(config.channel_id)

            except FloodWait as e:
                print(e, e.value)
                time.sleep(e.value)
                i -= 1
            except ChatForwardsRestricted:

                file = await app.download_media(m, in_memory=True, progress=progress)

                if m.document is not None:
                    await app.send_document(config.channel_id, file)
                elif m.voice is not None:
                    await app.send_voice(config.channel_id, file, progress=progress)
                elif m.video_note is not None:
                    await app.send_video_note(config.channel_id, file)
                elif m.audio is not None:
                    await app.send_audio(config.channel_id, file)

            except Exception as e:
                print(m)
                print(e, last_message)

        else:
            last += 1
            print(i)

        i += 1

app.run(main())
