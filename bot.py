import asyncio
from aiogram import Bot, Dispatcher
from frontend import handlers_register
from backend import marks_api
import aioschedule
from backend.databases.database import Database

async def main():
    db = await Database.setup()
    bot = Bot(token=await db.get_bot_token(), parse_mode='html')
    await db.close_connection()
    dp = Dispatcher(bot)
    await handlers_register.setup(dp)
    await bot.delete_webhook(drop_pending_updates=True)
    asyncio.create_task(scheduler())
    await dp.start_polling(bot)

async def scheduler():
    #aioschedule.every(2).minutes.do(marks_api.update_marks)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())