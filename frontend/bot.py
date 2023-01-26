import asyncio
from aiogram import Bot, Dispatcher
import handlers_register

async def main():
    bot = Bot(token="5719666199:AAFmsqG46O4zzfsR-scdtBB-NHgo2v8W6qI")
    dp = Dispatcher(bot)
    await handlers_register.setup(dp)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())