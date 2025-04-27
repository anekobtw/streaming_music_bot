from aiogram import F, Router, types
from aiogram.filters import Command

from enums import Messages

router = Router()


@router.message(F.text, Command("start"))
async def start(message: types.Message) -> None:
    await message.answer(Messages.START_MESSAGE.value["ru"])
