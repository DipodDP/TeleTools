from pyrogram.types import Message

from app_init import app_init
from config import load_config

app = app_init()
config = load_config()


@app.on_message()
async def my_handler(client, message: Message):
    m = await app.get_messages(message.chat.id, message.id)
    channel_id = config.channel_id
    print(m)
    caption = m.caption if m.caption is not None else ''
    if m.from_user is not None:
        caption = f'{caption}\nFrom:' \
                  f'{(" " + m.from_user.first_name) if m.from_user.first_name is not None else ""}' \
                  f'{(" " + m.from_user.last_name) if m.from_user.last_name is not None else ""}'

    if m.sender_chat is not None:
        m.sender_chat.has_protected_content = False
        m.sender_chat.id = channel_id
        m.sender_chat.title = f'{caption}\n{m.sender_chat.title}'
        # m.sender_chat.is_creator = False
    m.chat.id = channel_id
    if m.chat.title is not None:
        caption = f'{caption}\n{m.chat.title}'
        m.chat.title = ''
    # m.author_signature = caption
    # m.description = caption
    m.caption = caption
    m.chat.has_protected_content = False
    m.text = (m.text + "\n" + caption) if m.text is not None else None
    print(caption)

    await m.copy(config.channel_id)


print('Retranslator is running')
app.run()
