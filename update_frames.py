# uses the satnogs api to update frames in a db ater a full export
# will be set up with cron as a command so all you have to do is give a norad id and update duration as two int values and it'll do the rest

import requests
import time
import env_vars
import time
import calendar
import os
import sqlquery
import argparse
import datetime

# make sure to add automatic start_time/end_time for update telemetry
# add parameter telling function how many days to subtract from current date for automatic start_time/end_time


satnogs_api_token = env_vars.satnogs_api_token
script_dir = env_vars.script_dir


def genTimestamps(update_duration: int, offset: int):
    if not os.path.exists(f"{script_dir}/logs/update_frames.log"):
        with open(f"{script_dir}logs/update_frames.log", "w") as logfile:
            logfile.write(f"{datetime.datetime.now()}: Generating timestamps.")
    # logger
    else:
        with open(f"{script_dir}/logs/update_frames.log", "a") as logfile:
            logfile.write(f"\n{datetime.datetime.now()}: Generating timestamps.")

    year_before = False
    current_datetime = str(datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f%Z"))[:19]
    date_and_time = current_datetime[5:10]
    timestamps = [current_datetime[5:10], current_datetime[5:10]]
    differences = [int(int(date_and_time[3:]) - update_duration - offset), int(int(date_and_time[3:]) - offset)]
    print(differences)

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
        "12": 31,
    }

    for i in range(2):
        if differences[i] <= 0:
            if differences[i] == 0:
                if calendar.isleap(int(current_datetime[:4])) and timestamps[i][:2] == "03":
                    timestamps[i] = "02-29"
                if timestamps[i][:2] == "01":
                    timestamps[i] = "12-31"
                    year_before = True
                else:
                    timestamps[i] = f"{timestamps[i][:2]}{days_per_month[timestamps[i][:2]]}"

            else:
                if calendar.isleap(int(current_datetime[:4])) and timestamps[i][:2] == "03":
                    old_date = days_per_month["02"] + differences[i] + 1
                    timestamps[i] = f"02-{old_date}"

                if timestamps[i][:2] == "01":
                    old_month = "12"
                    old_date = str(days_per_month[old_month] + differences[i])
                    if len(old_date) == 1:
                        old_date = f"0{old_date}"
                    timestamps[i] = f"{old_month}-{old_date}"
                    year_before = True

                else:
                    old_month = str(int(timestamps[i][:2]) - 1)
                    if len(old_month) == 1:
                        old_month = f"0{old_month}"
                    old_date = str(days_per_month[old_month] + differences[i])
                    if len(old_date) == 1:
                        old_date = f"0{old_date}"
                    timestamps[i] = f"{old_month}-{old_date}"

            if year_before:
                old_year = int(current_datetime[:4] - 1)
                timestamps[i] = f"{old_year}-{timestamps[i]}{current_datetime[10:]}"

            else:
                timestamps[i] = f"{current_datetime[:5]}{timestamps[i]}{current_datetime[10:]}"

        else:
            if len(str(differences[i])) == 1:
                timestamps[i] = f"{current_datetime[:8]}0{str(differences[i])}{current_datetime[10:]}"

            else:
                timestamps[i] = f"{current_datetime[:8]}{str(differences[i])}{current_datetime[10:]}"

    start_time = f"{timestamps[0]}Z"
    end_time = f"{timestamps[1]}Z"

    if not os.path.exists(f"{script_dir}/logs/update_frames.log"):
        with open(f"{script_dir}/logs/update_frames.log", "w") as logfile:
            logfile.write(f"\n{datetime.datetime.now()}: Start timestamp generated: {start_time}")
    # logger
    else:
        with open(f"{script_dir}/logs/update_frames.log", "a") as logfile:
            logfile.write(f"\n{datetime.datetime.now()}: Start timestamp generated: {start_time}")

    if not os.path.exists(f"{script_dir}/logs/update_frames.log"):
        with open(f"{script_dir}logs/update_frames.log", "w") as logfile:
            logfile.write(f"\n{datetime.datetime.now()}: End timestamp generated: {end_time}")
    # logger
    else:
        with open(f"{script_dir}/logs/update_frames.log", "a") as logfile:
            logfile.write(f"\n{datetime.datetime.now()}: End timestamp generated: {end_time}")

    print("Done\n")
    return start_time, end_time


def updateTelemetry(norad_id: int, start_time: str, end_time: str):
    try_again = True
    sat_url = f"https://db-dev.satnogs.org/api/satellites/?norad_cat_id={norad_id}"
    response = requests.get(url=sat_url, headers={"Authorization": "Token" + satnogs_api_token})

    if response.json()[0]["status"] != "alive":
        sqlquery.sql().notInOrbit(norad_id)
        quit

    while try_again:
        try:
            url = f"https://db.satnogs.org/api/telemetry/?satellite={norad_id}&start={start_time}&end={end_time}"

            response = requests.get(url=url, headers={"Authorization": "Token " + satnogs_api_token})
            # all the json telemetry
            raw_data = response.json()
            frames = []
            timestamps = []
            stations = []
            norad_ids = []

            for i in range(len(raw_data)):
                # if raw_data[i]["frame"] not in frames:
                # create log file if it doesn't exist
                if not os.path.exists(f"{script_dir}/logs/update_frames.log"):
                    with open(f"{script_dir}logs/update_frames.log", "w") as logfile:
                        logfile.write(f"\n{datetime.datetime.now()}: Appending frame: " + raw_data[i]["frame"])
                # logger
                else:
                    with open(f"{script_dir}/logs/update_frames.log", "a") as logfile:
                        logfile.write(f"\n{datetime.datetime.now()}: Appending frame: " + raw_data[i]["frame"])
                if not os.path.exists(f"{script_dir}/logs/update_frames.log"):
                    with open(f"{script_dir}logs/update_frames.log", "w") as logfile:
                        logfile.write(f"\n{datetime.datetime.now()}: Appending timestamp: " + raw_data[i]["timestamp"])
                # logger
                else:
                    with open(f"{script_dir}/logs/update_frames.log", "a") as logfile:
                        logfile.write(f"\n{datetime.datetime.now()}: Appending timestamp: " + raw_data[i]["timestamp"])
                frames.append(raw_data[i]["frame"])
                if not os.path.exists(f"{script_dir}/logs/update_frames.log"):
                    with open(f"{script_dir}logs/update_frames.log", "w") as logfile:
                        logfile.write(f"\n{datetime.datetime.now()}: Total number of frames: {len(frames)}")
                # logger
                else:
                    with open(f"{script_dir}/logs/update_frames.log", "a") as logfile:
                        logfile.write(f"\n{datetime.datetime.now()}: Total number frames: {len(frames)}")
                date_time = str(raw_data[i]["timestamp"])
                date_time = date_time.replace("Z", "")
                date_time = date_time.replace("T", " ")
                timestamp = calendar.timegm(time.strptime(date_time, "%Y-%m-%d %H:%M:%S"))
                timestamps.append(timestamp)
                if not os.path.exists(f"{script_dir}/logs/update_frames.log"):
                    with open(f"{script_dir}logs/update_frames.log", "w") as logfile:
                        logfile.write(f"\n{datetime.datetime.now()}: Appending station: " + raw_data[i]["observer"])
                # logger
                else:
                    with open(f"{script_dir}/logs/update_frames.log", "a") as logfile:
                        logfile.write(f"\n{datetime.datetime.now()}: Appending station: " + raw_data[i]["observer"])
                stations.append(raw_data[i]["observer"])

            # check for next page
            next_page_available = "Link" in response.headers.keys()
            if next_page_available:
                header_parts = response.headers["Link"].split(",")
                for part in header_parts:
                    if part[-5:-1] == "next":
                        next_page_url = part[1:-13]

            frame_count = len(frames)
            while next_page_available:
                # delay avoids throttling
                if frame_count > 70:
                    if not os.path.exists(f"{script_dir}/logs/update_frames.log"):
                        with open(f"{script_dir}logs/update_frames.log", "w") as logfile:
                            logfile.write(f"\n{datetime.datetime.now()}: Delay to prevent throttling.")
                    # logger
                    else:
                        with open(f"{script_dir}/logs/update_frames.log", "a") as logfile:
                            logfile.write(f"\n{datetime.datetime.now()}: Delay to prevent throttling.")
                    time.sleep(17)
                    if not os.path.exists(f"{script_dir}/logs/update_frames.log"):
                        with open(f"{script_dir}logs/update_frames.log", "w") as logfile:
                            logfile.write(f"\n{datetime.datetime.now()}: Delay finished.")
                    # logger
                    else:
                        with open(f"{script_dir}/logs/update_frames.log", "a") as logfile:
                            logfile.write(f"\n{datetime.datetime.now()}: Delay finished.")

                response = requests.get(url=next_page_url, headers={"Authorization": "Token " + satnogs_api_token})
                next_page = response.json()
                for i in range(len(next_page) - 1):
                    frame_count += 1
                    if not os.path.exists(f"{script_dir}/logs/update_frames.log"):
                        with open(f"{script_dir}logs/update_frames.log", "w") as logfile:
                            logfile.write(f"\n{datetime.datetime.now()}: Checking frame: {frame_count}")
                    # logger
                    else:
                        with open(f"{script_dir}/logs/update_frames.log", "a") as logfile:
                            logfile.write(f"\n{datetime.datetime.now()}: Checking frame: {frame_count}")
                # filter frames and timestamps and append them to the final list
                for i in range(len(raw_data)):
                    # create log file if it doesn't exist
                    if not os.path.exists(f"{script_dir}/logs/update_frames.log"):
                        with open(f"{script_dir}logs/update_frames.log", "w") as logfile:
                            logfile.write(f"\n{datetime.datetime.now()}: Appending frame: " + raw_data[i]["frame"])
                    # logger
                    else:
                        with open(f"{script_dir}/logs/update_frames.log", "a") as logfile:
                            logfile.write(f"\n{datetime.datetime.now()}: Appending frame: " + raw_data[i]["frame"])
                    if not os.path.exists(f"{script_dir}/logs/update_frames.log"):
                        with open(f"{script_dir}logs/update_frames.log", "w") as logfile:
                            logfile.write(f"\n{datetime.datetime.now()}: Appending timestamp: " + raw_data[i]["timestamp"])
                    # logger
                    else:
                        with open(f"{script_dir}/logs/update_frames.log", "a") as logfile:
                            logfile.write(f"\n{datetime.datetime.now()}: Appending timestamp: " + raw_data[i]["timestamp"])
                    frames.append(raw_data[i]["frame"])
                    if not os.path.exists(f"{script_dir}/logs/update_frames.log"):
                        with open(f"{script_dir}logs/update_frames.log", "w") as logfile:
                            logfile.write(f"\n{datetime.datetime.now()}: Total number of frames: {len(frames)}")
                    # logger
                    else:
                        with open(f"{script_dir}/logs/update_frames.log", "a") as logfile:
                            logfile.write(f"\n{datetime.datetime.now()}: Total number frames: {len(frames)}")
                    date_time = str(raw_data[i]["timestamp"])
                    date_time = date_time.replace("Z", "")
                    date_time = date_time.replace("T", " ")
                    timestamp = calendar.timegm(time.strptime(date_time, "%Y-%m-%d %H:%M:%S"))
                    timestamps.append(timestamp)
                    if not os.path.exists(f"{script_dir}/logs/update_frames.log"):
                        with open(f"{script_dir}logs/update_frames.log", "w") as logfile:
                            logfile.write(f"\n{datetime.datetime.now()}: Appending station: " + raw_data[i]["observer"])
                    # logger
                    else:
                        with open(f"{script_dir}/logs/update_frames.log", "a") as logfile:
                            logfile.write(f"\n{datetime.datetime.now()}: Appending station: " + raw_data[i]["observer"])
                    stations.append(raw_data[i]["observer"])

                next_page_available = False

                if "Link" in response.headers.keys():
                    parts = response.headers["Link"].split(",")
                    for part in parts:
                        if part[-5:-1] == "next":
                            next_page_url = part[1:-13]
                            next_page_available = True

            # if no frames are available don't do anything
            if len(frames) == 0:
                # create log file if it doesn't exist
                if not os.path.exists(f"{script_dir}/logs/update_frames.log"):
                    with open(f"{script_dir}/logs/update_frames.log", "w") as logfile:
                        logfile.write(f"{datetime.datetime.now()}: No frames were retrieved. Here's the server response for more details: {response.json()}")
                # logger
                else:
                    with open(f"{script_dir}/logs/update_frames.log", "a") as logfile:
                        logfile.write(f"\n{datetime.datetime.now()}: No frames were retrieved. Here's the server response for more details: {response.json()}")
                exit

            else:
                if not os.path.exists(f"{script_dir}/logs/update_frames.log"):
                    with open(f"{script_dir}/logs/update_frames.log", "w") as logfile:
                        logfile.write(f"\n{datetime.datetime.now()}: Total number of frames: {len(frames)}")
                # logger
                else:
                    with open(f"{script_dir}/logs/update_frames.log", "a") as logfile:
                        logfile.write(f"\n{datetime.datetime.now()}: Total number of frames: {len(frames)}")
            print("Total number of frames:", len(frames))
            print(" ")

            for i in range(len(frames) - 1):
                norad_ids.append(norad_id)

            # make it so timestamps and corresponding frames go from least to greatest
            frames.reverse()
            timestamps.reverse()
            stations.reverse()
            try_again = False
            return norad_ids, timestamps, frames, stations

        except requests.exceptions.ConnectionError:
            # create log file if it doesn't exist
            if not os.path.exists(f"{script_dir}/logs/update_frames.log"):
                with open(f"{script_dir}logs/update_frames.log", "w") as logfile:
                    logfile.write(f"{datetime.datetime.now()}: No frames were retrieved due to a network error. The system will try again.")
            # logger
            else:
                with open(f"{script_dir}/logs/update_frames.log", "a") as logfile:
                    logfile.write(f"\n{datetime.datetime.now()}: No frames were retrieved due to a network error. The system will try again.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Update frames for a satellite using NORAD ID.")
    parser.add_argument("norad_id", type=int, help="NORAD ID of the satellite")
    parser.add_argument("update_duration", type=int, help="The span of days the satellite will fetch frames from. Going over a week or two is not reccomended.")
    parser.add_argument("offset", type=int, help="The date offset used to calculate timestamps. Going over a week or two is not recommended.")
    args = parser.parse_args()
    print("Generating timestamps")
    start_time, end_time = genTimestamps(update_duration=args.update_duration, offset=args.offset)
    print(f"Fetching frames from {start_time} to {end_time}")
    norad_ids, timestamps, frames, stations = updateTelemetry(norad_id=args.norad_id, start_time=start_time, end_time=end_time)
    if not os.path.exists(f"{script_dir}/logs/update_frames.log"):
        with open(f"{script_dir}logs/update_frames.log", "w") as logfile:
            logfile.write(f"\n{datetime.datetime.now()}: Generating SQL cursor.")
    # logger
    else:
        with open(f"{script_dir}/logs/update_frames.log", "a") as logfile:
            logfile.write(f"\n{datetime.datetime.now()}: Generating SQL cursor.")
    if not os.path.exists(f"{script_dir}/logs/update_frames.log"):
        with open(f"{script_dir}logs/update_frames.log", "w") as logfile:
            logfile.write(f"\n{datetime.datetime.now()}: Appending frames to DB.")
    # logger
    else:
        with open(f"{script_dir}/logs/update_frames.log", "a") as logfile:
            logfile.write(f"\n{datetime.datetime.now()}: Appending frames DB.")
    print("Appending frames to DB")
    sqlquery.sql().appendTelemetry(norad_ids=norad_ids, timestamps=timestamps, frames=frames, stations=stations)
    if not os.path.exists(f"{script_dir}/logs/update_frames.log"):
        with open(f"{script_dir}logs/update_frames.log", "w") as logfile:
            logfile.write(f"\n{datetime.datetime.now()}: Succesfully retrieved and appended frames in the span of {start_time} to end {end_time}.")
    # logger
    else:
        with open(f"{script_dir}/logs/update_frames.log", "a") as logfile:
            logfile.write(f"\n{datetime.datetime.now()}: Succesfully retrieved and appended frames in the span of {start_time} to end {end_time}.")
    print("Done")
