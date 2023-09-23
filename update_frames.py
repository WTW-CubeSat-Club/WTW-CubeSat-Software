#uses the satnogs api to update frames in a db ater a full export
#will be set up with cron as a command so all you have to do is give a norad id and it'll do the rest

import requests
import time
import env_vars
import time
import calendar
import os
import sqlquery
import argparse
from datetime import date

#make sure to add automatic start_time/end_time for update telemetry



satnogs_api_token = env_vars.satnogs_api_token
script_dir = env_vars.script_dir

 
def update_telemetry(norad_id:int, start_time, end_time):

    try_again = True
    while try_again:

        try:

    
            url = f'https://db.satnogs.org/api/telemetry/?satellite={norad_id}&start={start_time}&end={end_time}'


            response = requests.get(url=url, headers={'Authorization': 'Token ' + satnogs_api_token})
            #all the json telemetry
            raw_data = response.json()
            frames = []
            timestamps = []
            for i in range(len(raw_data)-1):
                if raw_data[i]["frame"] not in frames:
                    print(raw_data[i]["frame"])
                    print(raw_data[i]["timestamp"])
                    frames.append(raw_data[i]["frame"])
                    date_time = raw_data[i]["timestamp"]
                    date_time = date_time.replace("Z", "")
                    date_time = date_time.replace("T", " ")
                    timestamp = calendar.timegm(time.strptime(date_time, '%Y-%m-%d %H:%M:%S'))
                    timestamps.append(timestamp)


            #check for next page
            next_page_available = ('Link' in response.headers.keys())
            if next_page_available:
                header_parts = response.headers['Link'].split(',')
                for part in header_parts:
                    if part[-5:-1] == 'next':
                        next_page_url = part[1:-13]


            frame_count = len(frames)
            while next_page_available:
                #delay avoids throttling
                if frame_count > 70:
                    time.sleep(17)
                    print("delay")
                response = response = requests.get(url=next_page_url, headers={'Authorization': 'Token ' + satnogs_api_token})
                next_page = response.json()
                for i in range(len(next_page)-1):
                    frame_count+=1
                    print(next_page[i])
                    print(frame_count)
                #filter frames and timestamps and append them to the final list
                for i in range(len(raw_data)-1):
                    if raw_data[i]["frame"] not in frames:
                        print(raw_data[i]["frame"])
                        print(raw_data[i]["timestamp"])
                        frames.append(raw_data[i]["frame"])
                        print(raw_data[i]["timestamp"])
                        date_time = str(raw_data[i]["timestamp"])
                        date_time = date_time.replace("Z", "")
                        date_time = date_time.replace("T", " ")
                        timestamp = calendar.timegm(time.strptime(date_time, '%Y-%m-%d %H:%M:%S'))
                        timestamps.append(timestamp)

                next_page_available = False

                if 'Link' in response.headers.keys():
                    parts = response.headers['Link'].split(',')
                    for part in parts:
                        if part[-5:-1] == 'next':
                            next_page_url = part[1:-13]
                            next_page_available = True

            #if no frames are available don't do anything
            if len(frames) == 0:
                #create log file if it doesn't exist
                if not os.path.exists(f"{script_dir}logs/update_frames.log"):
                    with open(f"{script_dir}logs/update_frames.log", 'w') as logfile:
                        logfile.write(f"{date.today()}: No frames were retrieved. Here's the server response for more details: {response.json()}")
                #logger
                else:
                    with open(f"{script_dir}logs/update_frames.log", 'a') as logfile:
                        logfile.write(f"\n{date.today()}: No frames were retrieved. Here's the server response for more details: {response.json()}")
                exit
        
            print("len frames", len(frames))

            #make it so timestamps and corresponding frames go from least to greatest
            frames.reverse()
            timestamps.reverse()
            try_again = False
            return timestamps, frames

        except:
            #create log file if it doesn't exist
            if not os.path.exists(f"{script_dir}logs/update_frames.log"):
                with open(f"{script_dir}logs/update_frames.log", 'w') as logfile:
                    logfile.write(f"{date.today()}: No frames were retrieved due to a network error. The system will try again.")
            #logger
            else:
                with open(f"{script_dir}logs/update_frames.log", 'a') as logfile:
                    logfile.write(f"\n{date.today()}: No frames were retrieved due to a network error. The system will try again.")
        


#timestamps, frames = update_telemetry(25544, "2021-01-30T22:28:09Z", "2021-02-15T22:28:09Z")
#print(timestamps)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Update frames for a satellite using NORAD ID.")
    parser.add_argument('norad_id', type=int, help='NORAD ID of the satellite')
    args = parser.parse_args()

    timestamps, frames = update_telemetry(str(args.norad_id))
    console = sqlquery.sql(str(args.norad_id))
    console.append(timestamps, frames)

