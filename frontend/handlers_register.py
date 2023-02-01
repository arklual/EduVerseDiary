from frontend.handlers.general import general_handler
from frontend.handlers.marks import marks_handler
from frontend.handlers.homework import homework_handler

async def setup(dp, bot):
    #await marks_handler.setup(dp)
    await general_handler.setup(dp)
    await homework_handler.setup(dp, bot)