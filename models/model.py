from .orm import Base, MediaClass, ChannelClass


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


def create_movie(post_id: int, file_id: str, caption: str) -> int:
    data = movie.get_movie(file_id)
    if not data:
        movie.create_data(post_id, file_id, caption)
        return post_id
    else:
        return data.get('post_id', None)


def get_movie(post_id: int):
    data = movie.get_data(post_id)
    if data:
        return [data['file_id'], data['caption']]
    else:
        return False


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

def delete_movie(post_id: int):
    data = movie.get_data(post_id=post_id)
    if data:
        try:
            movie.delete_movie(post_id=post_id)
            return f"Kino muvaffaqiyatli o'chirildi ✅"
        except:
            return f"Kino o'chrishda xatolik yuzaga keldi ❌"
    else:
        return f"{post_id} - ID bilan kino topilmadi ❌"


# Channel table data
def create_channel(username: str, channel_id: str):
    data = channel.get_data(channel_id=channel_id)
    if data:
        return False
    else:
        channel.create_data(username, channel_id)
        return True
    

def delete_channel(channel_id: str):
    data = channel.get_data(channel_id)
    if data:
        channel.delete_data(channel_id)
        return True
    else:
        return None


def get_channels():
    data = channel.get_datas()
    text = f"Hamkor Kanallar ro'yhati 📥\n\n"
    for i in data:
        text += f"{i['username']}\n"
    return text


def get_channels_all():
    return channel.get_datas()
