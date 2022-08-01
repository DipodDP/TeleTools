
from pyrogram.types import Message

from app_init import app_init, verify_logger_group


app = app_init()

verify_logger_group(app)


@app.on_message()
async def my_handler(client, message: Message):
    m = await app.get_messages(message.chat.id, message.id)
    print(m)
    # ID чата
    chat_id = str(m.chat.id)
    # Получаем ID Юзера
    # print(repr(m))

    sender_id = m.sender_chat.id if 'from_user' not in repr(m) else m.from_user.id
    # Получаем ID сообщения
    msg_id = m.id
    # Получаем юзера
    sender = m.from_user.username if 'from_user' in repr(m) else 'Channel'
    # Получаем имя юзера
    from_name = ' '.join([str(m.from_user.first_name),
                          str(m.from_user.last_name)]) if 'from_user' in repr(m) else 'Channel'
    # print(m.from_user.first_name, m.from_user.last_name)
    # получаем имя группы
    chat_title = m.chat.title if 'title' in repr(m.chat) else m.chat.username

    # полчаем текст сообщения
    msg = ['*no text message*'] if m.text is None else m.text.split('\n')
    msg = msg[0]
    with open("Chat_log.txt", 'a', encoding='utf-8') as f:
        f.writelines(f"ID: {m.date} {chat_id} {chat_title} >>  "
                     f"(ID: {sender_id})  {from_name} ({sender}) - (ID: {msg_id}) {msg}\n")
    print(f"ID: {m.date} {chat_id} {chat_title} >>  (ID: {sender_id})  {from_name} ({sender}) - (ID: {msg_id}) {msg}")


print('Tele_log is running')
app.run()
