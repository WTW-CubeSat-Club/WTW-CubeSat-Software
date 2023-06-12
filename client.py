import asyncio
import websockets
import pathlib
import ssl
import subprocess
import os
import matplotlib.pyplot as plt
import csv
from _thread import start_new_thread as thread

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
localhost_pem = pathlib.Path(__file__).with_name("test.pem")
ssl_context.load_verify_locations(localhost_pem)

async def socket():
    async with websockets.connect('wss://localhost:8000', ssl=ssl_context) as websocket:
        while True:    
            command = input("Command: ")
            await websocket.send(command)
            global start_time
            start_time = input("Start time: ")
            await websocket.send(start_time)
            end_time = input("End time: ")
            await websocket.send(end_time)
            data_type = input("Data type: ")
            await websocket.send(data_type)
            print("\n")
            global unparsed
            unparsed = await websocket.recv()
            print("\n")
            print("[OK]\n")
            break
        
def parse(list):
    reader = csv.reader(list.splitlines(), quoting=csv.QUOTE_NONNUMERIC)
    global y_list
    y_list = next(reader)
    global y_len
    y_len = len(y_list)

def graph(x_list, y_list):
    plt.plot(x_list, y_list, 'o')
    plt.show()

def makeXList(start_time):
    x_list = []
    for i in range(y_len):
        start_time = int(start_time)
        x_list.append(start_time)
        start_time+=1
    return x_list

def clear():
    if os.name == "nt":
        subprocess.run("cls")
    else:
        subprocess.run("clear")

def saveData(x_list, y_list):
    ask = input("Save data? [y/n]: ")
    if ask.lower() == 'y':
        filename = input("Enter the filename: ")
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(x_list)
            writer.writerow(y_list)
        print("Data saved successfully!")
    else:
        print("Data not saved.")

def main():
    subprocess.run("clear")
    while True:
        start = input("[Press a key to connect]")
        clear()
        print("\n")
        asyncio.get_event_loop().run_until_complete(socket())
        parse(unparsed)
        x_list = makeXList(start_time)
        print("[Close window to send another command]")
        graph(x_list, y_list)
        saveData(x_list, y_list)
        clear()

if __name__ == "__main__":
    main()
