from os import getenv
from celery import Celery
from main import bot
from models.model import get_users

celery_app = Celery('my_celery_tasks', broker='redis://localhost:6379/0')

@celery_app.task
async def send_advertisement(msg):
    try:
        summa = 0
        users = get_users()
        admin_id = int(getenv("ADMIN"))

        for user in users:
            if int(user['telegram_id']) != admin_id:
                try:
                    print(user['telegram_id'])
                    await msg.copy_to(int(user['telegram_id']), caption=msg.caption, caption_entities=msg.caption_entities, reply_markup=msg.reply_markup)
                except Exception as e:
                    print(f"Send Error: {e}")
                    summa += 1

        await bot.send_message(admin_id, text=f"Botni bloklagan Userlar soni: {summa}")

    except Exception as e:
        print(f"Error: {e}")
