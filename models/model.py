import requests
from .orm import Base, MediaClass, ChannelClass
from os import getenv
from dotenv import load_dotenv

load_dotenv()
user = Base("users")
channel = ChannelClass("channels")
movie = MediaClass("movies")

# User table data


def create_user(telegram_id: int):
    data = user.get_data(str(telegram_id))
    if not data:
        user.create_data(telegram_id=str(telegram_id))
        return True
    else:
        return False


def get_users():
    return user.get_datas()


def statistika_user():
    data = user.statistika()
    all_data = user.get_datas()
    if data:
        return (f"Admin uchun Userlar statistikasi 📊\n\n"
                f"Oxirgi 30 kun ichida ro'yhatdan o'tgan userlar soni: {len(data['month'])}\n"
                f"Oxirgi 7 kun ichida ro'yhatdan o'tgan userlar soni: {len(data['week'])}\n"
                f"Oxirgi 24 soat ichida ro'yhatdan o'tgan userlar soni: {len(data['day'])}\n\n"
                f"Barcha Userlar soni: {len(all_data)}")
    else:
        return False

# Movies table data


def create_movie(file_id: str, caption: str) -> int:
    data = movie.get_movie(file_id)
    if not data:
        movie.create_data(file_id, caption)
        tables = []
        for mov in movie.get_datas():
            tables.append(mov['post_id'])
        post_id = max(tables)
        return post_id
    else:
        return data.get('post_id', None)


def get_movie(post_id: int):
    data = movie.get_data(post_id)
    if data:
        return [data['file_id'], data['caption']]
    else:
        return None


def statistika_movie():
    data = movie.statistika()
    all_data = movie.get_datas()
    if data:
        return (f"Admin uchun Kinolar statistikasi 📊\n\n"
                f"Oxirgi 30 kun ichida yuklangan kinolar soni: {len(data['month'])}\n"
                f"Oxirgi 7 kun ichida yuklangan kinolar soni: {len(data['week'])}\n"
                f"Oxirgi 24 soat ichida yuklangan kinolar soni: {len(data['day'])}\n\n"
                f"Barcha Kinolar soni: {len(all_data)}")
    else:
        return False


# Channel table data
def create_channel(username: str):
    data = channel.get_data(username)
    if data:
        return False
    else:
        channel.create_data(username)
        return True


def delete_channel(username: str):
    data = channel.get_data(username)
    if data:
        channel.delete_data(username)
        return True
    else:
        return None


def check_channels(telegram_id: int):
    TOKEN = getenv("TOKEN")
    channels = channel.get_datas()
    summa = 0
    for i in channels:
        url = f'https://api.telegram.org/bot{TOKEN}/getChatMember?chat_id=@{i[1]}&user_id={telegram_id}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            chat_member_status = data.get('result', {}).get('status', '')
            if chat_member_status in ["administrator", 'member', 'creator']:
                summa += 1
        else:
            break
    return True if summa == len(channels) else False


def get_channels():
    data = channel.get_datas()
    text = f"Hamkor Kanallar ro'yhati 📥\n\n"
    for i in data:
        text += f"@{i['username']}\n"
    return text
