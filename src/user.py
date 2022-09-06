import json

from database import connection
from song import Song


class User:

    def __init__(self, username: str):
        data = connection.execute("SELECT username, music_count, last_songs FROM users WHERE username=?", [username.lower()]).fetchone()
        if data is None:
            connection.execute("INSERT INTO users (username) VALUES (?)", [username.lower()])
            connection.commit()
            data = connection.execute("SELECT username, music_count, last_songs FROM users WHERE username=?", [username.lower()]).fetchone()
        self._username: str = data[0]
        self.music_count: int = data[1]
        self.last_songs: list[int] = json.loads(data[2])
        self.last_song_cache: Song = None

    def song_heard(self, song: Song):
        song.listen()
        if self.last_song_cache is None:
            self.last_song_cache = song
        else:
            self.last_song_cache.add_after_song(song)
            self.last_song_cache = song
        self.last_songs.append(song.id)
        if len(self.last_songs) > 50:
            self.last_songs.pop(0)
        self.music_count += 1
        connection.execute("UPDATE users SET music_count=?, last_songs=? WHERE username=?",
                           [self.music_count, json.dumps(self.last_songs), self._username]
                           )
        connection.commit()

    @property
    def username(self) -> str:
        return self._username.capitalize()
