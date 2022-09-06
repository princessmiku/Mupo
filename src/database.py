import sqlite3

connection = sqlite3.connect("./data/music.sqlite3", check_same_thread=False, cached_statements=2)
