#!/usr/bin/env python

import asyncio
import websockets

async def hello():
    uri = "wss://localhost:8765"
    async with websockets.connect(uri) as websocket:
        time = input("Start time, end time: ")
        await websocket.send(time)
        data_type = input("Data type: ")
        await websocket.send(data_type)

        await websocket.recv()
        await asyncio.Future()



if __name__ == "__main__":
    asyncio.run(hello())