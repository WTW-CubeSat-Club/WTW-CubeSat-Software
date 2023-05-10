import sqlite3

conn = sqlite3.connect("data.db")
c = conn.cursor()

c.execute("""CREATE TABLE temp (
    unix_time integer,
    data real
)""")

c.execute("""CREATE TABLE airpressure (
    unix_time integer,
    data real
)""")

c.execute("""CREATE TABLE altitude (
    unix_time integer,
    data real
)""")