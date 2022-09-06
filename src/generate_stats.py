import json
import threading
import time

from colorama import Fore
from tqdm import tqdm

from database import connection
import random

from song import Song
from user import User

users = [User(username[0]) for username in connection.execute("SELECT username FROM users").fetchall()]
songs = [Song(tId[0]) for tId in connection.execute("SELECT id FROM titles").fetchall()]

m_s_unter = 300  # untere stunden anzahl
m_s_durchschnitt = 2000  # durchschnitts stunden anzahl eines nutzers welcher 2 jahre musik hört ca
m_s_oberste = 7000  # höchste stunden anzahl

pBar = tqdm(users, bar_format=Fore.YELLOW + "Generate Data Structure | {l_bar} {bar:20} {r_bar}")


def userAction(user: User):
    n = random.triangular(m_s_unter, m_s_oberste, m_s_durchschnitt)
    to_listen = round(n * 60 / 3)
    for __ in range(to_listen):
        song: Song = random.choice(songs)
        user.song_heard(song)
    pBar.update(1)


threads = [threading.Thread(target=userAction, args=(user,), daemon=True) for user in users]
[thread.start() for thread in threads]
[thread.join() for thread in threads]


def saveData():
    [
        connection.execute(
            "UPDATE titles SET after=?, hears=? WHERE id=?",
            [json.dumps(song.after), song.hears, song.id]
        ) for song in songs
    ]
    [
        connection.execute(
            "UPDATE users SET last_songs=?, music_count=? WHERE username=?",
            [json.dumps(user.last_songs), user.music_count, user._username]
        ) for user in users
    ]
    connection.commit()


saveData()
