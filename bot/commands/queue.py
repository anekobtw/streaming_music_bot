import asyncio
import os

import aiohttp
from aiogram import F, Router, types
from mutagen.easyid3 import EasyID3
from mutagen.id3 import APIC, ID3
from yt_dlp import YoutubeDL

from enums import APIs, Keyboards, Messages

router = Router()


@router.callback_query(F.data.startswith("queue_"))
async def queue(callback: types.CallbackQuery) -> None:
    _, action, index = callback.data.split("_")
    print(action, index)
