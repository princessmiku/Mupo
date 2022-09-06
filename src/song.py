import json

from database import connection



class Song:

    def __init__(self, _id: int, title: str = None, artist: str = None, year: int = None, after: str = None, hear: int = None):
        data = connection.execute(f"SELECT title, artist, year, after, hears FROM titles WHERE id = ?", [_id]).fetchone()
        if data is None: raise ValueError("No song data found under id " + str(_id))
        self.id: int = _id
        self.title: str = data[0] if title is None else title
        self.artist: str = data[1] if artist is None else artist
        self.year: str = data[2] if year is None else year
        self.after: dict = json.loads(data[3]) if after is None else json.loads(after)
        self.hears: int = data[4] if hear is None else hear

    def add_after(self, _id: int):
        if not self.after.__contains__(str(_id)):
            self.after[str(_id)] = 1
        else:
            self.after[str(_id)] += 1
        connection.execute("UPDATE titles SET after=? WHERE id=?", [json.dumps(self.after), self.id])
        connection.commit()

    def add_after_song(self, song):
        self.add_after(song.id)

    def listen(self):
        self.hears += 1
        connection.execute("UPDATE titles SET hears=? WHERE id=?", [self.hears, self.id])
        connection.commit()
