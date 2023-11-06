import asyncio
import datetime

from aiogram import Bot, Dispatcher
from frontend import handlers_register
import middleware
import aioschedule
from backend.databases.database import Database
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from backend import homework_api, marks_api

async def main():
    db = await Database.setup()
    bot = Bot(token=await db.get_bot_token(), parse_mode='html')
    storage = MemoryStorage()
    await db.close_connection()
    dp = Dispatcher(bot, storage=storage)
    await handlers_register.setup(dp)
    await bot.delete_webhook(drop_pending_updates=True)
    asyncio.create_task(scheduler(bot))
    sender = middleware.Sender(bot)
    await sender.send_new_marks()
    await homework_api.update_hash()
    #await marks_api.get_final_marks()
    await dp.start_polling(bot)




async def scheduler(bot):
    sender = middleware.Sender(bot)
    aioschedule.every(10).minutes.do(sender.send_new_marks)
    aioschedule.every(15).minutes.do(homework_api.update_hash)
    aioschedule.every(1).day.at('14:00').do(sender.egetime_send)
    #aioschedule.every(1).hour.do(marks_api.get_final_marks)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())
