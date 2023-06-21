import asyncio
import websockets
import pathlib
import ssl
import sys
import subprocess
import matplotlib.pyplot as plt
import csv
import time
if sys.platform == "darwin":
    from applescript import tell
import pexpect


ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
localhost_pem = pathlib.Path(__file__).with_name("test.pem")
ssl_context.load_verify_locations(localhost_pem)

#find current directory
pwd = subprocess.check_output("pwd")
pwd = str(pwd).replace("'", "")
pwd = pwd[1:]
pwd = pwd[:len(pwd)-2]

def clear():
    if sys.platform == "win32" or sys.platform == "cygwin" or sys.platform == "msys":
        subprocess.run("cls")
    else:
        subprocess.run("clear")

async def socket():
    #error tells program if conection succeeded or not
    global error
    error = True
    localcmds = ["tracker"]
    global command
    command = input("\nCommand: ").lower().replace(" ", "")
    if command in localcmds:
        error = False

    if command not in localcmds:
        try:
            async with websockets.connect('wss://localhost:8000', ssl=ssl_context) as websocket:
                while True:
                    clear()
                    print("\n[Ground station client]")
                    #lowercase and get rid of spaces
                    await websocket.send(command)
                    global start_time
                    #get rid of spaces
                    start_time = input("Start time: ").replace(" ", "")
                    await websocket.send(start_time)
                    #get rid of spaces
                    end_time = input("End time: ").replace(" ", "")
                    await websocket.send(end_time)
                    #lower and get rid of spaces
                    global data_type
                    data_type = input("Data type: ").lower().replace(" ", "")
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
        except websockets.exceptions.ConnectionClosedError:
            clear()
            print("\n[Parameters are invalid]")
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
    print("\n[Ground station client]")
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
        print("\n[Ground station client]")
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
    print("[Ground station client]")
    asyncio.get_event_loop().run_until_complete(socket())
    clear()

def startTracker(sat_id):
    if sys.platform == "linux" or sys.platform == "linux2":
        command = f'python {pwd}/sattracker.py'
        subprocess.Popen('xterm -hold -e "%s"' % command)
    if sys.platform == "darwin":
        terminalcommand= f"conda activate satcom && SATID={sat_id} python {pwd}/sattracker.py"
        tell.app('Terminal', 'do script "' + terminalcommand + '"') 





def main():
    clear()
    try:
        #run client forever
        while True:
            #start client
            clear()
            start = input("\n[Press enter to start]")
            clear()
            #set norad id for sattracker.py in environment variable so sattracker can see it
            print("\n[Ground station client]")
            sat_id = input("\nSatellite ID: ").replace(" ", "")
            clear()
            #set variable that controls while loop
            #while loop enables mutiple commands to one db
            again = "y"
            while again == "y":

                connect()

                if error == False:
                    print("\n[OK]")
                    time.sleep(1)
                    clear()
                    if command.lower() == "get":
                        if data_type != "images" or data_type != "pictures":
                            parse(unparsed)
                            x_list = makeXList(start_time)
                            graph(x_list, y_list)
                            clear()
                            clear()
                            saveData(x_list, y_list)
                            clear()
                        else:
                            #will add stuff to deal with images later
                            pass

                    if command.lower().replace(" ", "") == "tracker":
                        startTracker(sat_id)
                        clear()
                if error == False:
                    another_cmd = input("\nSend another command? [y/n]: ")
                    clear()
                    another_cmd = another_cmd.replace(" ", "")
                    if another_cmd.lower() != "y":
                        again = another_cmd
    
                    else:
                        break
                    

    except KeyboardInterrupt:
        clear()
        print("\n[Quitting]")
        time.sleep(0.6)
        tell.app( 'Terminal', 'do script "' + "kill -9 $(ps -p $PPID -o ppid=)" + '"')
        clear()
        quit



if __name__ == "__main__":
    main()
