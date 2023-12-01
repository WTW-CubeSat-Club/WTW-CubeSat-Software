import requests
from datetime import datetime
import time
from client import clear
import env_vars_client as env_vars


""" 
note:
    there is a request limit set per hour, and if you go over it
    the website will deny requests and you will get an error
 """


#observer latitude (decimal degrees)
lat = env_vars.lat

#observer longitude (decimal degrees)
lng = env_vars.lng

#set observer elevation above sea level (meters)
elevation = env_vars.elevation


# num of future positions to return, don't mess with this variable because it doesn't really matter much to the function, but it is still needed
sec = "1"

#num of days for pass prediction
days = env_vars.days

#minimum number of seconds sat should be visible, set at 3 mins by default
min_visibility = env_vars.min_visibility

#api key
api_key = env_vars.ny2o_api_key

#update in secs
update = env_vars.update

#run socket
#asyncio.get_event_loop().run_until_complete(recieveStop())

#gonna be recieving NORAD ID from client
#this is just a test
#sat_id = os.environ.get("SATID")
sat_id = 27865



def main(sat_id:int):
                

    try:
        #keep trying to reconnect
        while True:
            try:
                try:

                    #need to copy code here so we can let the user know its initializing and not clear the whole screen later on
                    #that way ui can update fast and without the user noticing
                    clear()
                    print("\n[Retrieving data]")
                    current_data_req = requests.get(
                        url=f"https://api.n2yo.com/rest/v1/satellite/positions/{sat_id}/{lat}/{lng}/{elevation}/{sec}/&apiKey={api_key}")
                    pass_data_req = requests.get(
                        url=f"https://api.n2yo.com/rest/v1/satellite/visualpasses/{sat_id}/{lat}/{lng}/{elevation}/{days}/{min_visibility}/&apiKey={api_key}")
                    first = True
                    clear()

                    while True:
                        #if samedb == "1":
                        #nested try statement because connection error might occur multiple times
            
                        try:
                            retrive = True
                            #checks to see if it needs to retrive and skips block if its run for the first time
                            while retrive and not first:
                                start_time=time.time()
                                current_data_req = requests.get(
                                    url=f"https://api.n2yo.com/rest/v1/satellite/positions/{sat_id}/{lat}/{lng}/{elevation}/{sec}/&apiKey={api_key}")
                                pass_data_req = requests.get(
                                    url=f"https://api.n2yo.com/rest/v1/satellite/visualpasses/{sat_id}/{lat}/{lng}/{elevation}/{days}/{min_visibility}/&apiKey={api_key}")
                                end_time=time.time()-start_time
                                #takes care of error for when update is at or below 1
                                try:
                                    time.sleep(update - end_time)
                                except:
                                    time.sleep(0.3)
                                retrive = False
                    
                            #converts raw data into json
                            current_data = current_data_req.json()
                            pass_data = pass_data_req.json()
                            first = False
                        
                            #parsing
                            satname = current_data["info"]["satname"]
                            satalt = round(int(current_data["positions"][0]["sataltitude"]) * 3280.8)
                            satlat = current_data["positions"][0]["satlatitude"]
                            satlng = current_data["positions"][0]["satlongitude"]
                
                            clear()
                            print("\n[Tracker]\n")
                            print(f"Satellite name: {satname}")
                            print(f"NORAD ID: {sat_id}")
                            print(f"Current coordinates: {satlat}, {satlng}")
                            print(f"Current altitude: {satalt} ft\n")
                            print("[Pass Prediction]\n")
                            # get passes data
        
                            try:
                                timestamp = pass_data["passes"][0]["startUTC"]
                                start_time = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
                                duration = pass_data["passes"][0]["duration"]
                                minutes = int(duration) // 60
                                seconds = int(duration) % 60
                                num_passes = pass_data["info"]["passescount"]
                                end_timestamp = timestamp + duration 
                                #show data
                        
                                if timestamp-time.time() <= 0 and  end_timestamp < time.time():
                                    print("Currently overhead: yes")
                                else:
                                    print("Currently overhead: no")
                            
                                print(f"Future passes over the next {days} days: {num_passes}")
                                print(f"Time of next pass: {start_time}")
                                print(f"Duration of next pass: {minutes} mins, {seconds} secs")

                            except:
                                print(f"No available pass data for the next {days} days")

                        except (requests.exceptions.JSONDecodeError, KeyError, IndexError):
                            clear()
                            print("\n[Error occurred while parsing data]")
                            time.sleep(3)
                            clear()

                except requests.exceptions.RequestException:
                    secs = 10
                    for i in range(10):
                        clear()
                        print(f"\n[Could not connect, retrying in {secs} secs]")
                        secs -= 1
                        time.sleep(0.95)
                
            #catch control c when it's retrieving data
            except KeyboardInterrupt:
                clear()
                print("\n[Quitting]")
                time.sleep(0.6)
                clear()
                quit()
                    
    except:
        clear()
        print("\n[Quitting]")
        time.sleep(0.6)
        clear()


if __name__ == "__main__":
    main(sat_id)
