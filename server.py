#!/usr/bin/env python

import asyncio
import websockets
import sqlite3
import time

#establishing sqlite cursor and db connection
conn = sqlite3.connect("data.db")
c = conn.cursor()

class sql:

    #no init method needed
    def get(start_time, end_time, data_type):
        #find data_type and set which table we are querying, using single quotes so sqlite doesn't get confused
        if data_type == "temp":
            while start_time <= end_time:
                #convert into str because sqlite is picky like that
                str_time = "%s" % start_time
                print(str_time)
                c.execute("""SELECT unix_time, data FROM temp WHERE unix_time = ?""", [str_time])
                print(c.fetchall())
                start_time+=1
        if data_type == "altitude":
            while start_time <= end_time:
                #convert into str because sqlite is picky like that
                str_time = "%s" % start_time
                c.execute("""SELECT * FROM altitude WHERE unix_time = ?""", [str_time])
                print(c.fetchall())
                start_time+=1

    def append(data_type, data):
        #using if statements so I don't have to interpolate the data_type
        for i in range(1):
            if data_type == "temp":
                c.execute("""INSERT INTO temp VALUES (?, ?)""", (round(time.time()), data))
            if data_type == "altitude":
                c.execute("""INSERT INTO altitude VALUES (?, ?)""", (round(time.time()), data))
            if data_type == "airpressure":
                c.execute("""INSERT INTO temp VALUES (?, ?)""", (round(time.time()), data))
            else:
                print("invalid data type")
            conn.commit()
"""
async def hello(websocket):
    
    command = await websocket.recv()
    print(f"<<< {command}")

    await websocket.send(command)
    #f allows insertion of a param
    print(f">>> {command}")

"""

async def hello(websocket):
    console = sql()
    await websocket.send("Command: ")
    command = await websocket.recv()
    #data pipe and satellite communication protocol is still not known
    
    if command == "get":
        time = await websocket.recv()
        start_time, end_time= time.split(",")
        print(start_time)
        print(end_time)
        data_type = await websocket.recv()
        print(data_type)
        await websocket.send("done")
        print(data_type)
      #  await websocket.send(console.get(start_time, end_time))

async def main():
    #with is a shortened try finally block
    async with websockets.serve(hello, "localhost", 8765):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())