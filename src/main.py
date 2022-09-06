import time
from typing import Union

from rich.console import Console
from rich.table import Table

from database import connection
from pri import prefix_loading, prefix_select, clearing, startup_text, prefix_login
from song import Song
from tqdm import tqdm
from colorama import Fore

from user import User

print(startup_text)
print(prefix_login + "Please enter a username for your login")
username = input(" " * 8)
username = username.lower()

time.sleep(0.5)
isBack = True if connection.execute("SELECT username FROM users WHERE username=?", [username]).fetchone() else False
user = User(username)
if isBack:
    print(prefix_login + "Welcome back " + username.capitalize() + "! Enjoy the system ")
else:
    print(prefix_login + "Welcome " + username.capitalize() + "! Try the system out")
time.sleep(1)
print(prefix_login + "One moment... the system is initializing")
time.sleep(3)
clearing()
list_of_songs = []
# einfach damit es cool aussieht
ids = connection.execute("SELECT id FROM titles WHERE year >= 2000 LIMIT 10").fetchall()
__lenOfId = len(ids)

pbar = tqdm(ids, bar_format=prefix_loading + Fore.YELLOW + "Load songs from the database | {l_bar} {bar:20} {r_bar}")
for i in pbar:
    i = i[0]
    time.sleep(0.02)
    song: Song = Song(i)
    list_of_songs.append(song)
    if i == ids[-1][0]:
        pbar.bar_format = prefix_loading + Fore.GREEN + "Load songs from the database | {l_bar} {bar:20} {r_bar}"
time.sleep(2)
clearing()
# After loading all


def displayTables():
    songList = Table(title="Page with Titles")
    songList.add_column("ID")
    songList.add_column("Title", style="cyan")
    songList.add_column("Artist", style="magenta")
    songList.add_column("Release", justify="right", style="green")
    for song in list_of_songs:
        songList.add_row(str(song.id), song.title, song.artist, str(song.year))
    songList.add_row("---", "Your last heard songs", " ", "----")
    for song_id in user.last_songs[-5:]:
        song = Song(song_id)
        songList.add_row(str(song.id), song.title, song.artist, str(song.year))
    if user.last_song_cache:
        songList.add_row("---", "Song suggestions\nbased on the last song", " ", "----")
        last_song: Song = user.last_song_cache
        sorted_keys = sorted(last_song.after.keys(), reverse=True)
        for key in sorted_keys[:5]:
            sl_song = Song(int(key))
            songList.add_row(str(sl_song.id), sl_song.title, sl_song.artist, str(sl_song.year))
    console = Console()
    console.print(songList, justify="left")


def song_not_found(_id: Union[int, str] = "?"):
    clearing()
    print(Fore.RED + "The song with the id", str(_id), "was not found")
    time.sleep(2)
    clearing()


def wrong_input():
    clearing()
    print(Fore.RED + "This input is incorrect")
    time.sleep(2)
    clearing()


def wait_input_and_handle():
    print(prefix_select + "Write the id of an song from the list: ")
    song_input: str = input(prefix_select)
    if not song_input.isnumeric():
        wrong_input()
        return
    if not connection.execute("SELECT id FROM titles WHERE id=?", [int(song_input)]).fetchone():
        song_not_found(song_input)
        return
    dSong = Song(int(song_input))
    print(prefix_select + "Song found, the song is called", dSong.title, "from the artist", dSong.artist)
    time.sleep(2)
    user.song_heard(dSong)
    print(prefix_select + "The song is now heard, please select a new one")
    time.sleep(2)


# running things
p_run = True


if __name__ == '__main__':
    while p_run:
        print(Fore.RESET)
        displayTables()
        wait_input_and_handle()
        # finish clean up
        clearing()

