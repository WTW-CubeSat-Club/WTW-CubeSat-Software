import asyncio
import websockets
import pathlib
import ssl
 
ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
localhost_pem = pathlib.Path(__file__).with_name("test.pem")
ssl_context.load_verify_locations(localhost_pem)

async def test():
    async with websockets.connect('wss://localhost:8000', ssl=ssl_context) as websocket:
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
