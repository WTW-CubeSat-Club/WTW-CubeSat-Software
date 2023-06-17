import asyncio
import websockets
import pathlib
import ssl
import sys
import subprocess
import matplotlib.pyplot as plt
import csv
import time


ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
localhost_pem = pathlib.Path(__file__).with_name("test.pem")
ssl_context.load_verify_locations(localhost_pem)

def clear():
    if sys.platform == "win32" or sys.platform == "cygwin" or sys.platform == "msys":
        subprocess.run("cls")
    else:
        subprocess.run("clear")

async def socket():
    global error
    error = True
    
    try:
        async with websockets.connect('wss://localhost:8000', ssl=ssl_context) as websocket:
            while True:
                clear()
                command = input("\nCommand: ")
                await websocket.send(command)
                global start_time
                start_time = input("Start time: ")
                await websocket.send(start_time)
                end_time = input("End time: ")
                await websocket.send(end_time)
                data_type = input("Data type: ")
                await websocket.send(data_type)
                global unparsed
                unparsed = await websocket.recv()
                error = False
                break
    
    #display error if connect fails
    except OSError:
        clear()
        print("\n[Could  not connect]")
        time.sleep(1.5)
    
    #display error for invalid params
    except:
        clear()
        print("\n[Parameters are invalid, try again]")
        time.sleep(1.5)
        
#parse y list given as a string
def parse(list):
    reader = csv.reader(list.splitlines(), quoting=csv.QUOTE_NONNUMERIC)
    global y_list
    y_list = next(reader)
    global y_len
    y_len = len(y_list)

#graph x and y lists
def graph(x_list, y_list):
    ask = input("\nGraph data? [y/n]: ")
    if ask.lower() == "y":
        clear()
        print("\n[Close window to continue]")
        plt.plot(x_list, y_list, 'o')
        plt.show()
    
#make x list based on start time and end time
def makeXList(start_time):
    x_list = []
    for i in range(y_len):
        start_time = int(start_time)
        x_list.append(start_time)
        start_time+=1
    return x_list


#save data
def saveData(x_list, y_list):
    try:
        ask = input("\nSave data? [y/n]: ")
        if ask.lower() == 'y':
            filename = input("Enter the filename: ")
            #make sure it's saved as csv
            filename = filename+".csv"
            with open(filename, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(x_list)
                writer.writerow(y_list)
                clear()
                print("\n[OK]")
                time.sleep(1)

    #error catching
    except:
        clear()
        print("\n[Error, data not saved]")
        time.sleep(1)

#connect using socket function
def connect():
    start = input("\n[Press a key to connect]")
    clear()
    asyncio.get_event_loop().run_until_complete(socket())
    clear()


def main():
    clear()
    try:
        while True:
            connect()

            if error == False:
                print("\n[OK]")
                time.sleep(1)
                clear()
                parse(unparsed)
                x_list = makeXList(start_time)
                graph(x_list, y_list)
                clear()
                clear()
                saveData(x_list, y_list)
                clear()
    except KeyboardInterrupt:
        clear()
        print("\n[Quitting]")
        time.sleep(0.6)
        clear()
        quit

if __name__ == "__main__":
    main()
