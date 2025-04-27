from aiogram import F, Router, types
from aiogram.filters import Command

from enums import Databases, Messages

router = Router()


@router.message(F.text, Command("create"))
async def create(message: types.Message) -> None:
    room_id = Databases.ROOMS_DATABASE.value.create_room(message.from_user.id)
    await message.answer(f"<code>/join {room_id}</code>")


@router.message(F.text, Command("join"))
async def join(message: types.Message) -> None:
    room_id = message.text.split(" ")[1]

    if not Databases.ROOMS_DATABASE.value.room_exists(room_id):
        await message.answer(Messages.ROOM_DOESNT_EXISTS.value["ru"])
        return

    if Databases.ROOMS_DATABASE.value.is_user_in_room(room_id, message.from_user.id):
        await message.answer(Messages.ALREADY_JOINED.value["ru"])
        return

    Databases.ROOMS_DATABASE.value.add_user_to_room(room_id, message.from_user.id)
