import requests
from datetime import datetime
import time
from client import clear
import requests.exceptions



#set NORAD ID
clear()
# gonna eventually receive this from client.py
sat_id = input("\nSatellite ID: ")
clear()
#observer latitude (decimal degrees)
lat = "38.807780"

#observer longitude (decimal degrees)
lng = "-77.210430"

#set observer elevation above sea level (meters)
elevation = "82"


# num of future positions to return, don't mess with this variable because it doesn't really matter much to the func, but it is still needed
sec = "1"

#num of days for pass prediction
days = "9"

#minimum number of seconds sat should be visible, set at 3 mins for now
min_visibility = "180"

#api key
api_key = "enter api key"

#update in secs
update = 5

def main():
    try:
        while True:
            clear()
            print("\n[Retrieving data]")

            #nested try statement because connection error might occur multiple times
            try:
                try:
                    current_data_req = requests.get(
                        url=f"https://api.n2yo.com/rest/v1/satellite/positions/{sat_id}/{lat}/{lng}/{elevation}/{sec}/&apiKey={api_key}")
                    pass_data_req = requests.get(
                        url=f"https://api.n2yo.com/rest/v1/satellite/visualpasses/{sat_id}/{lat}/{lng}/{elevation}/{days}/{min_visibility}/&apiKey={api_key}")
                    pass_data = pass_data_req.json()
                    current_data = current_data_req.json()
            

                
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
                        start_time = datetime.fromtimestamp(pass_data["passes"][0]["startUTC"]).strftime('%Y-%m-%d %H:%M:%S')
                        duration = pass_data["passes"][0]["duration"]
                        minutes = int(duration) // 60
                        seconds = int(duration) % 60
                        num_passes = pass_data["info"]["passescount"]
                        #show data
                        print(f"Future passes over the next {days} days: {num_passes}")
                        print(f"Time of next pass: {start_time}")
                        print(f"Duration of next pass: {minutes} mins, {seconds} secs")

                    except:
                        print("No available pass data for the next {days} days")
                    time.sleep(update)

                except (requests.exceptions.JSONDecodeError, KeyError, IndexError):
                    print("\n[Error occurred while parsing data]")
                    time.sleep(5)

            except requests.exceptions.RequestException:
                secs = 10
                for i in range(9):
                    clear()
                    print(f"\n[Could not connect, retrying in {secs} secs]")
                    secs -= 1
                    time.sleep(0.95)
                

                    
    except KeyboardInterrupt:
        clear()
        print("\n[Quitting]")
        time.sleep(0.6)
        clear()


main()
