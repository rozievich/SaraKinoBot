import os
import logging
from dotenv import load_dotenv
from db.connect import startup_table
from aiogram import Bot, Dispatcher, types, executor
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from states.state_admin import AddMedia, ReklamaState, AddChannelState, DeleteChannelState
from models.model import create_user, get_users, get_movie, statistika_user, statistika_movie, create_movie, get_channels, create_channel, delete_channel, check_channels
from buttons.inline_keyboards import forced_channel
from buttons.reply_keyboards import admin_btn, channels_btn, movies_btn, exit_btn
from aiogram.contrib.fsm_storage.memory import MemoryStorage

load_dotenv()
logging.basicConfig(level=logging.INFO)
TOKEN = os.getenv("TOKEN")
bot = Bot(TOKEN)
dp = Dispatcher(bot=bot, storage=MemoryStorage())


@dp.message_handler(commands="start")
async def welcome_handler(msg: types.Message):
    create_user(msg.from_user.id)
    await bot.set_my_commands(commands=[types.BotCommand("start", "Ishga tushirish ♻️")])
    await bot.send_message(msg.chat.id, text=f"Assalomu alaykum {msg.from_user.first_name} 🤖\nSaraKinoBot - orqali siz o'zingizga yoqqani kinoni topishingiz mumkin 🎬\nShunchaki kino kodini yuboring va kinoni oling ✅")


@dp.message_handler(commands="panel")
async def admin_handler(msg: types.Message):
    if msg.from_user.id == int(os.getenv("ADMIN")):
        await msg.answer(f"Assalomu alaykum {msg.from_user.first_name} 🤖\nAdmin sahifaga xush kelibsiz ⚙️", reply_markup=admin_btn())
    else:
        await msg.answer("Siz admin emassiz ❌", reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(Text("Statistika 📊"))
async def user_statistika_handler(msg: types.Message):
    if msg.from_user.id == int(os.getenv("ADMIN")):
        await msg.answer(text=statistika_user(), reply_markup=admin_btn())
    else:
        await msg.answer("Siz admin emassiz ❌", reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(Text("Kinolar 🎬"))
async def media_statistika_handler(msg: types.Message):
    if msg.from_user.id == int(os.getenv("ADMIN")):
        await msg.answer("Kinolar kategoriyasiga xush kelibsiz 🛠", reply_markup=movies_btn())
    else:
        await msg.answer("Siz admin emassiz ❌", reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(Text("Kino Statistika 📊"))
async def kino_statistika_handler(msg: types.Message):
    if msg.from_user.id == int(os.getenv("ADMIN")):
        await msg.answer(text=statistika_movie(), reply_markup=movies_btn())
    else:
        await msg.answer("Siz admin emassiz ❌", reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(Text("Kino qo'shish 📥"))
async def kino_add_handler(msg: types.Message):
    if msg.from_user.id == int(os.getenv("ADMIN")):
        await AddMedia.media.set()
        await msg.answer("Kinoni yuborishingiz mumkin 🎬", reply_markup=exit_btn())
    else:
        await msg.answer("Siz admin emassiz ❌", reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(state=AddMedia.media, content_types=types.ContentType.VIDEO)
async def handle_video(msg: types.Message, state: FSMContext):
    if msg.text == "❌":
        await msg.answer("Kino yuklash bekor qilindi ❌", reply_markup=movies_btn())
        await state.finish()
    else:
        data = create_movie(file_id=msg.video.file_id, caption=msg.caption)
        if data:
            await msg.reply(f"Kino malumotlar bazasiga saqlandi ✅\nKino Kodi: {data}", reply_markup=movies_btn())
        await state.finish()


@dp.message_handler(Text("❌"))
async def exit_handler(msg: types.Message):
    if msg.from_user.id == int(os.getenv("ADMIN")):
        await msg.answer("Bosh menyu 🔮", reply_markup=admin_btn())


@dp.message_handler(Text("Kanallar 🖇"))
async def channels_handler(msg: types.Message):
    if msg.from_user.id == int(os.getenv("ADMIN")):
        await msg.answer(text=get_channels(), reply_markup=channels_btn())
    else:
        await msg.answer("Siz admin emassiz ❌", reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(Text("Kanal qo'shish ⚙️"))
async def add_channel_handler(msg: types.Message):
    if msg.from_user.id == int(os.getenv("ADMIN")):
        await AddChannelState.username.set()
        await msg.answer(text="Qo'shish kerak bo'lgan kanal Usernameni kiriting ✍️", reply_markup=exit_btn())
    else:
        await msg.answer("Siz admin emassiz ❌", reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(state=AddChannelState.username)
async def add_channel_handler_func(msg: types.Message, state: FSMContext):
    if msg.text == "❌":
        await msg.answer("Kanal qo'shish bekor qilindi ❌", reply_markup=channels_btn())
        await state.finish()
    else:
        data = create_channel(msg.text)
        if data:
            await msg.answer("Kanal muvaffaqiyatli qo'shildi ✅", reply_markup=channels_btn())
            await state.finish()
        else:
            await msg.answer("Bu kanal oldin qo'shilgan ❌", reply_markup=channels_btn())
            await state.finish()


@dp.message_handler(Text("Kanal o'chirish 🗑"))
async def movie_delete_handler(msg: types.Message):
    if msg.from_user.id == int(os.getenv("ADMIN")):
        await DeleteChannelState.username.set()
        await msg.answer(text="O'chirish kerak bo'lgan kanal Usernameni kiriting ✍️", reply_markup=exit_btn())
    else:
        await msg.answer("Siz admin emassiz ❌", reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(state=DeleteChannelState.username)
async def delete_channel_handler_func(msg: types.Message, state: FSMContext):
    if msg.text == "❌":
        await msg.answer("Kanal o'chirish bekor qilindi ❌", reply_markup=channels_btn())
        await state.finish()
    else:
        data = delete_channel(msg.text)
        if data:
            await msg.answer("Kanal muvaffaqiyatli o'chirildi ✅", reply_markup=channels_btn())
        else:
            await msg.answer("Bunday usernameli kanal mavjud emas ❌", reply_markup=channels_btn())
        await state.finish()


@dp.message_handler(Text("Reklama 🎁"))
async def reklama_handler(msg: types.Message):
    if msg.from_user.id == int(os.getenv("ADMIN")):
        await ReklamaState.rek.set()
        await bot.send_message(chat_id=msg.chat.id, text="Reklama tarqatish bo'limi 🤖", reply_markup=exit_btn())
    else:
        await bot.send_message(chat_id=msg.chat.id, text="Siz admin emassiz ❌", reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(state=ReklamaState.rek, content_types=types.ContentType.ANY)
async def rek_state(msg: types.Message, state: FSMContext):
    if msg.text == "❌":
        await bot.send_message(chat_id=msg.chat.id, text="Reklama yuborish bekor qilindi 🤖❌", reply_markup=admin_btn())
        await state.finish()
    else:
        await bot.send_message(chat_id=msg.chat.id, text="Reklama yuborish boshlandi 🤖✅")
        summa = 0
        for i in get_users():
            if int(i['telegram_id']) != int(os.getenv("ADMIN")):
                try:
                    await msg.copy_to(int(i['telegram_id']), caption=msg.caption, caption_entities=msg.caption_entities, reply_markup=msg.reply_markup)
                except:
                    summa += 1
        await bot.send_message(int(os.getenv("ADMIN")), text=f"Botni bloklagan Userlar soni: {summa}", reply_markup=admin_btn())
        await state.finish()


@dp.callback_query_handler(lambda x: x.data == "channel_check")
async def channel_check_handler(callback: types.CallbackQuery):
    check = check_channels(callback.from_user.id)
    if check:
        await callback.message.delete()
    else:
        await callback.message.answer("Iltimos quidagi kanallarga obuna bo'ling", reply_markup=forced_channel())


@dp.message_handler(lambda x: x.text.isdigit())
async def forward_last_video(msg: types.Message):
    check = check_channels(msg.from_user.id)
    if check:
        data = get_movie(int(msg.text))
        if data:
            await bot.send_video(chat_id=msg.from_user.id, video=data[0], caption=f"{data[1]}\n\n🤖 Bizning bot: @Sarakinolar_bot")
        else:
            await msg.reply(f"{msg.text} - id bilan hech qanday kino topilmadi ❌")
    else:
        await msg.answer("Iltimos quidagi kanallarga obuna bo'ling", reply_markup=forced_channel())


async def startup(dp):
    startup_table()


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=startup, skip_updates=True)
