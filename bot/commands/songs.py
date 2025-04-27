import asyncio
import os

import aiohttp
from aiogram import F, Router, types
from mutagen.easyid3 import EasyID3
from mutagen.id3 import APIC, ID3
from yt_dlp import YoutubeDL

from enums import APIs, Keyboards, Messages

router = Router()

CACHE_FOLDER = os.path.join("songs")


@router.message(F.text)
async def search(message: types.Message) -> None:
    result = APIs.yt.value.search(query=message.text, filter="songs", limit=5)

    keyboard = []
    for song in result[:10]:
        keyboard.append([types.InlineKeyboardButton(text=f"{song['artists'][0]['name']} - {song['title']} | {song['duration']}", callback_data=f"song_{song['videoId']}")])

    await message.answer(Messages.SONGS_FOUND.value["ru"], reply_markup=types.InlineKeyboardMarkup(inline_keyboard=keyboard))


async def download_thumbnail(url: str, path: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                with open(path, "wb") as f:
                    f.write(await resp.read())


async def download_audio(url: str, out_path: str):
    def _blocking_download():
        ydl_opts = {"format": "bestaudio/best", "outtmpl": out_path, "postprocessors": [{"key": "FFmpegExtractAudio", "preferredcodec": "mp3", "preferredquality": "192"}], "quiet": True}
        with YoutubeDL(ydl_opts) as ydl:
            return ydl.extract_info(url, download=True)

    info = await asyncio.to_thread(_blocking_download)
    return info


async def embed_metadata(audio_path: str, thumb_path: str, info: dict):
    audio = EasyID3(audio_path)
    audio["title"] = info.get("title", "Unknown Title")
    audio["artist"] = info.get("uploader", "Unknown Artist")
    audio.save()

    if os.path.exists(thumb_path):
        audiofile = ID3(audio_path)
        with open(thumb_path, "rb") as albumart:
            audiofile.add(APIC(encoding=3, mime="image/jpeg", type=3, desc="Cover", data=albumart.read()))
        audiofile.save()


@router.callback_query(F.data.startswith("song_"))
async def song_page(callback: types.CallbackQuery) -> None:
    video_id = callback.data.split("_", 1)[1]
    cache_path = f"{CACHE_FOLDER}/{video_id}.mp3"
    thumb_path = f"{CACHE_FOLDER}/{video_id}.jpg"

    await callback.answer(Messages.DOWNLOADING.value["ru"], show_alert=False)

    if not os.path.exists(cache_path):
        url = f"https://www.youtube.com/watch?v={video_id}"

        try:
            info = await download_audio(url, f"{CACHE_FOLDER}/{video_id}.%(ext)s")

            thumbnail_url = info.get("thumbnail")
            if thumbnail_url:
                await download_thumbnail(thumbnail_url, thumb_path)

            await embed_metadata(cache_path, thumb_path, info)

        except Exception as e:
            await callback.message.answer(f"Error: {e}")
            return

    await callback.message.answer_audio(audio=types.FSInputFile(cache_path), thumbnail=types.FSInputFile(thumb_path) if os.path.exists(thumb_path) else None, reply_markup=Keyboards.song_keyboard(video_id, "ru"))
