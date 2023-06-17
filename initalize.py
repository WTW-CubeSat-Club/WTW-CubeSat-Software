import sqlite3

#will add code for creating new databases for each norad id soon


conn = sqlite3.connect("data.db")
c = conn.cursor()


c.execute("""CREATE TABLE IF NOT EXISTS temp (
    unix_time integer,
    data real
)""")

c.execute("""CREATE TABLE IF NOT EXISTS airpressure (
    unix_time integer,
    data real
)""")

c.execute("""CREATE TABLE IF NOT EXISTS altitude (
    unix_time integer,
    data real
)""")

c.execute("""CREATE TABLE IF NOT EXISTS images (
    unix_time integer,
    data blob
)""")

conn.commit()