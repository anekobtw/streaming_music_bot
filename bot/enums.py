from enum import Enum

from aiogram import types
from ytmusicapi import YTMusic

from db import RoomsDatabase


class Messages(Enum):
    START_MESSAGE = {"ru": "Привет!", "en": "Hi!"}
    ROOM_DOESNT_EXISTS = {"ru": "Комната не существует", "en": "Room doesn't exists"}
    ALREADY_JOINED = {"ru": "Вы уже в комнате", "en": "You are already in the room"}

    SONGS_FOUND = {"ru": "Найденные песни", "en": "Found songs"}
    DOWNLOADING = {"ru": "Скачивание...", "en": "Downloading..."}


class Databases(Enum):
    ROOMS_DATABASE = RoomsDatabase()


class Keyboards(Enum):
    def room_keyboard(room_id: str, lang: str) -> types.InlineKeyboardMarkup:
        texts = {
            "ru": {
                "delete": "Удалить комнату",
                "next": "Следующая песня",
                "prev": "Предыдущая песня",
            },
            "en": {
                "delete": "Delete room",
                "next": "Next song",
                "prev": "Previous song",
            },
        }[lang]

        return types.InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    types.InlineKeyboardButton(text=texts["prev"], callback_data=f"prev_song_{room_id}"),
                    types.InlineKeyboardButton(text=texts["next"], callback_data=f"next_song_{room_id}"),
                ],
                [types.InlineKeyboardButton(text=texts["delete"], callback_data=f"delete_room_{room_id}")],
            ]
        )

    def song_keyboard(song_id: str, lang: str) -> types.InlineKeyboardMarkup:
        texts = {
            "ru": {
                "add": "Добавить в очередь",
                "remove": "Удалить из очереди",
            },
            "en": {
                "add": "Add to queue",
                "remove": "Remove from queue",
            },
        }[lang]

        return types.InlineKeyboardMarkup(
            inline_keyboard=[
                [types.InlineKeyboardButton(text=texts["add"], callback_data=f"queue_add_{song_id}")],
                [types.InlineKeyboardButton(text=texts["remove"], callback_data=f"queue_remove_{song_id}")],
            ]
        )


class APIs(Enum):
    yt = YTMusic()
