from app_init import app_init


app = app_init()

username = input('Enter username or user_id (one or list): ')
with app:
    user_id = app.get_users(username).id

print(user_id)
