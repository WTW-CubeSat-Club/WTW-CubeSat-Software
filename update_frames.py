#uses the satnogs api to update frames in a db ater a full export
#will be set up with cron as a command so all you have to do is give a norad id and update duration as two int values and it'll do the rest

import requests
import time
import env_vars
import time
import calendar
import os
import sqlquery
import argparse
import datetime

#make sure to add automatic start_time/end_time for update telemetry
#add parameter telling function how many days to subtract from current date for automatic start_time/end_time



satnogs_api_token = env_vars.satnogs_api_token
script_dir = env_vars.script_dir


def genTimestamps(update_duration:int):


    current_datetime = str(datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f%Z"))[:19]
    date_and_time = current_datetime[5:10]

   
    days_per_month = {

        "01": 31,
        "02": 28,
        "03": 31,
        "04": 30,
        "05": 31,
        "06": 30,
        "07": 31,
        "08": 31, 
        "09": 30, 
        "10": 31,
        "11": 30,
        "12": 31
        
        }
    
    difference = int(date_and_time[3:]) - update_duration
    if difference <= 0:
        if difference ==0:
            if calendar.isleap(int(current_datetime[:4])) and date_and_time[:2] == "03":
                date_and_time = "02-29"
            else:
                date_and_time = f"{date_and_time[:2]}{days_per_month[date_and_time[:2]]}"

        
            

        else:
            if calendar.isleap(int(current_datetime[:4])) and date_and_time[:2] == "03":
                old_date = days_per_month["02"] + difference + 1
                date_and_time = f"02-{old_date}"
            
            else:
                old_month = str(int(date_and_time[:2]) -1)
                if len(old_month) == 1:
                    old_month = f"0{old_month}"
                old_date = str(days_per_month[old_month] + difference)
                if len(old_date) == 1:
                    old_date = f"0{old_date}"
                date_and_time = f"{old_month}-{old_date}"

        past_time = f"{current_datetime[:5]}{date_and_time}{current_datetime[10:]}"

        

            
    else:
        if len(str(difference)) == 1:
            past_time = f"{current_datetime[:8]}0{str(difference)}{current_datetime[10:]}"
        else:
            past_time = f"{current_datetime[:8]}{str(difference)}{current_datetime[10:]}"

    start_time = f"{past_time}Z"
    end_time = f"{current_datetime}Z"

    return start_time, end_time


 
def updateTelemetry(norad_id:int, start_time:str, end_time:str):


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
                    print("delay")
                    time.sleep(17)
                response = requests.get(url=next_page_url, headers={'Authorization': 'Token ' + satnogs_api_token})
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
                if not os.path.exists(f"{script_dir}/logs/update_frames.log"):
                    with open(f"{script_dir}/logs/update_frames.log", 'w') as logfile:
                        logfile.write(f"{datetime.date.today()}: No frames were retrieved. Here's the server response for more details: {response.json()}")
                #logger
                else:
                    with open(f"{script_dir}logs/update_frames.log", 'a') as logfile:
                        logfile.write(f"\n{datetime.date.today()}: No frames were retrieved. Here's the server response for more details: {response.json()}")
                exit
        
            print("len frames", len(frames))

            #make it so timestamps and corresponding frames go from least to greatest
            frames.reverse()
            timestamps.reverse()
            try_again = False
            return timestamps, frames

        except:
            #create log file if it doesn't exist
            if not os.path.exists(f"{script_dir}/logs/update_frames.log"):
                with open(f"{script_dir}logs/update_frames.log", 'w') as logfile:
                    logfile.write(f"{datetime.date.today()}: No frames were retrieved due to a network error. The system will try again.")
            #logger
            else:
                with open(f"{script_dir}/logs/update_frames.log", 'a') as logfile:
                    logfile.write(f"\n{datetime.date.today()}: No frames were retrieved due to a network error. The system will try again.")
        


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Update frames for a satellite using NORAD ID.")
    parser.add_argument('norad_id', type=int, help='NORAD ID of the satellite')
    parser.add_argument('update_duration', type=int, help='The span of days the satellite will fetch frames from.')
    args = parser.parse_args()
    start_time, end_time = genTimestamps(args.update_duration)
    print(start_time, end_time)
    timestamps, frames = updateTelemetry(str(args.norad_id), start_time, end_time)
    print("\n\n\n"+timestamps+frames)
    #console = sqlquery.sql(str(args.norad_id))
    #console.append(timestamps, frames)

