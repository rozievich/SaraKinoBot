import os
import logging
from dotenv import load_dotenv
from db.connect import startup_table
from aiogram import Bot, Dispatcher, types, executor
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from states.state_admin import AddMedia, ReklamaState, AddChannelState, DeleteChannelState, DeleteMovieState
from models.model import create_user, get_movie, statistika_user, statistika_movie, create_movie, get_channels, create_channel, delete_channel, get_users, delete_movie, get_channels_all
from buttons.inline_keyboards import forced_channel
from buttons.reply_keyboards import admin_btn, channels_btn, movies_btn, exit_btn
from aiogram.contrib.fsm_storage.memory import MemoryStorage


load_dotenv(".env")
logging.basicConfig(level=logging.INFO)
TOKEN = os.getenv("TOKEN")
bot = Bot(TOKEN)
dp = Dispatcher(bot=bot, storage=MemoryStorage())
admin = os.getenv("ADMIN")


@dp.message_handler(commands="start")
async def welcome_handler(msg: types.Message):
    create_user(msg.from_user.id)
    await bot.set_my_commands(commands=[types.BotCommand("start", "Ishga tushirish ♻️")])
    await bot.send_message(msg.chat.id, text=f"Assalomu alaykum {msg.from_user.first_name} 🤖\n<b>Tarjimalar Tv Bot</b> - orqali siz o'zingizga yoqqan kinoni topishingiz mumkin 🎬\nShunchaki kino kodini yuboring va kinoni oling ✅", parse_mode=types.ParseMode.HTML)


@dp.message_handler(commands="panel")
async def admin_handler(msg: types.Message):
    if msg.from_user.id == int(admin):
        await msg.answer(f"Assalomu alaykum {msg.from_user.first_name} 🤖\nAdmin sahifaga xush kelibsiz ⚙️", reply_markup=admin_btn())
    else:
        await msg.answer("Siz admin emassiz ❌", reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(Text("Statistika 📊"))
async def user_statistika_handler(msg: types.Message):
    if msg.from_user.id == int(admin):
        await msg.answer(text=statistika_user(), reply_markup=admin_btn())
    else:
        await msg.answer("Siz admin emassiz ❌", reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(Text("Kinolar 🎬"))
async def media_statistika_handler(msg: types.Message):
    if msg.from_user.id == int(admin):
        await msg.answer("Kinolar kategoriyasiga xush kelibsiz 🛠", reply_markup=movies_btn())
    else:
        await msg.answer("Siz admin emassiz ❌", reply_markup=types.ReplyKeyboardRemove())
        
        
@dp.message_handler(Text("Kino Statistika 📊"))
async def kino_statistika_handler(msg: types.Message):
    if msg.from_user.id == int(admin):
        await msg.answer(text=statistika_movie(), reply_markup=movies_btn())
    else:
        await msg.answer("Siz admin emassiz ❌", reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(Text("Kino qo'shish 📥"))
async def kino_add_handler(msg: types.Message):
    if msg.from_user.id == int(admin):
        await AddMedia.media.set()
        await msg.answer("Kinoni yuborishingiz mumkin 🎬", reply_markup=exit_btn())
    else:
        await msg.answer("Siz admin emassiz ❌", reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(state=AddMedia.media, content_types=types.ContentType.ANY)
async def handle_video(msg: types.Message, state: FSMContext):
    try:
        if msg.text == "❌":
            await msg.answer("Kino yuklash bekor qilindi ❌", reply_markup=movies_btn())
            await state.finish()
        else:
            async with state.proxy() as data:
                data['file_id'] = msg.video.file_id
                data['caption'] = msg.caption
            await AddMedia.media_id.set()
            await msg.answer(text="Iltimos Kino uchun ID kiriting: ", reply_markup=exit_btn())
    except:
        await msg.answer("Iltimos Kino yuboring!", reply_markup=exit_btn())
    

@dp.message_handler(state=AddMedia.media_id, content_types=types.ContentType.TEXT)
async def handle_media_id(msg: types.Message, state: FSMContext):
    try:
        if msg.text == "❌":
            await msg.answer("Kino yuklash bekor qilindi ❌", reply_markup=movies_btn())
            await state.finish()
        elif not get_movie(int(msg.text)):
            async with state.proxy() as data:
                data['post_id'] = msg.text
                data = create_movie(post_id=int(data["post_id"]), file_id=data['file_id'], caption=data['caption'])
            if data:
                await msg.reply(f"Kino malumotlar bazasiga saqlandi ✅\nKino Kodi: {data}", reply_markup=movies_btn())
            await state.finish()
        else:
            await msg.reply(f"{msg.text} - ID bilan kino mavjud!")
    except:
        await msg.answer("Iltimos Kod sifatida Raqam yuboring!", reply_markup=exit_btn())


@dp.message_handler(Text("Kino o'chirish 🗑"))
async def handle_delete_media_func(msg: types.Message):
    if msg.from_user.id == int(admin):
        await DeleteMovieState.post_id.set()
        await msg.answer("Kinoni Kodini yuborishingiz mumkin 🎬", reply_markup=exit_btn())
    else:
        await msg.answer("Siz admin emassiz ❌", reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(state=DeleteMovieState.post_id)
async def handle_delete_media(msg: types.Message, state: FSMContext):
    try:
        if msg.text == "❌":
            await msg.answer("Kino o'chirish bekor qilindi ❌", reply_markup=movies_btn())
            await state.finish()
        else:
            data = delete_movie(int(msg.text))
            await msg.reply(text=data, reply_markup=movies_btn())
            await state.finish()
    except:
        await msg.answer("Iltimos Kod sifatida Raqam yuboring!", reply_markup=exit_btn())


@dp.message_handler(Text("Kanallar 🖇"))
async def channels_handler(msg: types.Message):
    if msg.from_user.id == int(admin):
        await msg.answer(text=get_channels(), reply_markup=channels_btn())
    else:
        await msg.answer("Siz admin emassiz ❌", reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(Text("Kanal qo'shish ⚙️"))
async def add_channel_handler(msg: types.Message):
    if msg.from_user.id == int(admin):
        await AddChannelState.username.set()
        await msg.answer(text="Qo'shish kerak bo'lgan kanal Usernameni kiriting ✍️", reply_markup=exit_btn())
    else:
        await msg.answer("Siz admin emassiz ❌", reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(state=AddChannelState.username)
async def add_channel_username_handler(msg: types.Message, state: FSMContext):
    try:
        if msg.text == "❌":
            await msg.answer("Kanal qo'shish bekor qilindi ❌", reply_markup=channels_btn())
            await state.finish()
        else:
            async with state.proxy() as data:
                data['username'] = msg.text
            await AddChannelState.channel_id.set()
            await msg.answer(text="Iltimos Kanal ID kiriting: ", reply_markup=exit_btn())
    except Exception as e:
        pass


@dp.message_handler(state=AddChannelState.channel_id)
async def add_channel_handler_func(msg: types.Message, state: FSMContext):
    if msg.text == "❌":
        await msg.answer("Kanal qo'shish bekor qilindi ❌", reply_markup=channels_btn())
        await state.finish()
    else:
        async with state.proxy() as data:
            data = create_channel(data['username'], msg.text)
        if data:
            await msg.answer("Kanal muvaffaqiyatli qo'shildi ✅", reply_markup=channels_btn())
            await state.finish()
        else:
            await msg.answer("Bu kanal oldin qo'shilgan ❌", reply_markup=channels_btn())
            await state.finish()


@dp.message_handler(Text("Kanal o'chirish 🗑"))
async def movie_delete_handler(msg: types.Message):
    if msg.from_user.id == int(admin):
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
    if msg.from_user.id == int(admin):
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
        await bot.send_message(chat_id=msg.chat.id, text="Reklama yuborish boshlandi 🤖✅", reply_markup=admin_btn())
        await state.finish()
        try:
            summa = 0
            for user in get_users():
                if int(user['telegram_id']) != int(admin):
                    try:
                        await msg.copy_to(int(user['telegram_id']), caption=msg.caption, caption_entities=msg.caption_entities, reply_markup=msg.reply_markup)
                    except Exception as e:
                        print(f"Send Error: {e}")
                        summa += 1
            await bot.send_message(int(admin), text=f"Botni bloklagan Userlar soni: {summa}")
        except Exception as e:
            print(f"Error: {e}")


@dp.callback_query_handler(lambda x: x.data == "channel_check")
async def channel_check_handler(callback: types.CallbackQuery):
    check = await check_sub_channels(callback.from_user.id)
    if check:
        await callback.message.delete()
        await callback.answer("Obuna bo'lganingiz uchun rahmat ☺️")
    else:
        await callback.message.answer("Iltimos quidagi kanallarga obuna bo'ling", reply_markup=forced_channel())


@dp.message_handler(Text("❌"))
async def exit_handler(msg: types.Message):
    if msg.from_user.id == int(admin):
        await msg.answer("Bosh menyu 🔮", reply_markup=admin_btn())


@dp.message_handler(lambda x: x.text.isdigit())
async def forward_last_video(msg: types.Message):
    check = await check_sub_channels(msg.from_user.id)
    if check:
        data = get_movie(int(msg.text))
        if data:
            try:
                await bot.send_video(chat_id=msg.from_user.id, video=data[0], caption=f"{data[1]}\n\n🤖 Bizning bot: @Tarjimalar_Tv_bot")
            except:
                await msg.reply(f"{msg.text} - id bilan hech qanday kino topilmadi ❌") 
        else:
            await msg.reply(f"{msg.text} - id bilan hech qanday kino topilmadi ❌")
    else:
        await msg.answer("Iltimos quidagi kanallarga obuna bo'ling", reply_markup=forced_channel())


async def check_sub_channels(user_id):
    channels = get_channels_all()
    for channel in channels:
        chat_member = await bot.get_chat_member(chat_id=int(channel[2]), user_id=user_id)
        if chat_member['status'] == 'left':
            print("Xato")
            return False
    return True


async def startup(dp):
    startup_table()


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=startup, skip_updates=True)
