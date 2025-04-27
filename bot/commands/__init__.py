from aiogram import Router

from . import room_manage, songs, start

router = Router()
router.include_router(start.router)
router.include_router(songs.router)
router.include_router(room_manage.router)
