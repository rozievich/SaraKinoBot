from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from models.model import channel


def forced_channel():
    channels = channel.get_datas()
    btn = InlineKeyboardMarkup(row_width=2)
    for i, v in enumerate(channels):
        btn.add(InlineKeyboardButton(f"{int(i) + 1} - kanal", url=f"{v['username']}"))
    return btn.add(InlineKeyboardButton("Tekshirish ✅", callback_data="channel_check"))
