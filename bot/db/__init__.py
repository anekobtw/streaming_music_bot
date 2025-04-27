import os
import sqlite3
from uuid import uuid4

database_path = os.path.join("db", "database.db")


class RoomsDatabase:
    def __init__(self) -> None:
        self.connection = sqlite3.connect(database_path)
        self.cursor = self.connection.cursor()

        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS rooms (
                room_id TEXT PRIMARY KEY,
                owner_id INTEGER NOT NULL,
                music_queue TEXTS,
                current_song_index INTEGER,
                users TEXT
            )
        """
        )

    def create_room(self, owner_id: int) -> None:
        room_id = str(uuid4())
        while self.room_exists(room_id):
            room_id = str(uuid4())
        self.cursor.execute("INSERT INTO rooms (room_id, owner_id, music_id, users) VALUES (?, ?, ?, ?)", (room_id, owner_id, -1, str(owner_id)))
        self.connection.commit()
        return room_id

    def room_exists(self, room_id: str) -> bool:
        self.cursor.execute("SELECT * FROM rooms WHERE room_id = ?", (room_id,))
        return self.cursor.fetchone() is not None

    def room_members(self, room_id: str) -> list[str]:
        self.cursor.execute("SELECT users FROM rooms WHERE room_id = ?", (room_id,))
        result = self.cursor.fetchone()
        return result[0].split(",") if result else []

    def is_user_in_room(self, room_id: str, user_id: int) -> bool:
        return str(user_id) in self.room_members(room_id)

    def add_user_to_room(self, room_id: str, user_id: str) -> None:
        users = self.room_members(room_id)
        if not self.is_user_in_room(room_id, user_id):
            users.append(str(user_id))
            self.cursor.execute("UPDATE rooms SET users = ? WHERE room_id = ?", (",".join(users), room_id))
            self.connection.commit()

    def room_owner(self, room_id: str) -> int:
        self.cursor.execute("SELECT owner_id FROM rooms WHERE room_id = ?", (room_id,))
        return int(self.cursor.fetchone()[0])

    def get_music_queue(self, room_id: str) -> list[str]:
        self.cursor.execute("SELECT music_queue FROM rooms WHERE room_id = ?", (room_id,))
        result = self.cursor.fetchone()
        return result[0].split(",") if result else []

    def add_song_to_queue(self, room_id: str, song_id: str) -> None:
        music_queue = self.get_music_queue(room_id)
        music_queue.append(song_id)
        self.cursor.execute("UPDATE rooms SET music_queue = ? WHERE room_id = ?", (",".join(music_queue), room_id))
        self.connection.commit()

    def clear_queue(self, room_id: str) -> None:
        self.cursor.execute("UPDATE rooms SET music_queue = ? WHERE room_id = ?", ("", room_id))
        self.connection.commit()

    def remove_song_from_queue(self, room_id: str, song_id: str) -> None:
        music_queue = self.get_music_queue(room_id)
        music_queue.remove(song_id)
        self.cursor.execute("UPDATE rooms SET music_queue = ? WHERE room_id = ?", (",".join(music_queue), room_id))
        self.connection.commit()

    def delete_room(self, room_id: str) -> None:
        self.cursor.execute("DELETE FROM rooms WHERE room_id = ?", (room_id,))
        self.connection.commit()
