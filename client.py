import asyncio
import websockets
 
async def test():
    async with websockets.connect('ws://localhost:8000') as websocket:
        while True:    
            command = input("Command: ")
            await websocket.send(command)
            start_time = input("Start time: ")
            await websocket.send(start_time)
            time = input("End time: ")
            await websocket.send(time)
            data_type = input("Data type: ")
            await websocket.send(data_type)
            print("\n")
            data = await websocket.recv()
            print(data)
            print("done")
            quit()
        
asyncio.get_event_loop().run_until_complete(test())

asyncio.get_event_loop().run_forever()