import asyncio
from aiogram import Bot, Dispatcher
from frontend import handlers_register
import middleware
import aioschedule
from backend.databases.database import Database
from aiogram.contrib.fsm_storage.memory import MemoryStorage


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
    await dp.start_polling(bot)

async def scheduler(bot):
    sender = middleware.Sender(bot)
    aioschedule.every(10).minutes.do(sender.send_new_marks)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())
