from handlers import general_handler, marks_handler, homework_handler

async def setup(dp):
    await general_handler.setup(dp)
    await marks_handler.setup(dp)
    await homework_handler.setup(dp)