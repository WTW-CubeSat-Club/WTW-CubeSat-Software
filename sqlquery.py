import time
import sqlite3
import os
import csv
import calendar
import requests
import mail

# import webbot
import env_vars
import os
import datetime
import operator
from pysqlcipher3 import dbapi2 as securesql

script_dir = env_vars.script_dir


def readCSV(norad_id: int):
    timestamps_raw = []
    frames_raw = []
    timestamps = []
    frames = []
    # opening the CSV file
    with open(f"{script_dir}/csv_cache/{norad_id}data.csv", mode="r") as file:
        # reading the CSV file
        csvFile = csv.reader(file)

        # displaying the contents of the CSV file
        for line in csvFile:
            str_line = line[0]
            split_line = str_line.split("|")
            timestamp = str(calendar.timegm(time.strptime(split_line[0], "%Y-%m-%d %H:%M:%S")))  # fix this to use zulu time
            timestamps_raw.append(timestamp)
            frames_raw.append(split_line[1])
        # remove duplicates
        for i in range(len(frames_raw) - 1):
            frames.append(frames_raw[i])
            timestamps.append(timestamps_raw[i])
    print(len(timestamps_raw))
    print(len(timestamps))
    # reverse lists to it can go from end time to start time
    timestamps.reverse()
    frames.reverse()
    os.remove(f"{script_dir}/csv_cache/{norad_id}data.csv")

    return timestamps, frames


class secureSQL:
    pass


class sql:
    db_folder = "data"
    db_name = "data"
    securedb_name = "private"
    db_path = f"{script_dir}/{db_folder}/{db_name}.db"
    securedb_path = f"{script_dir}/{db_folder}/{securedb_name}.db"

    def __init__(self):
        self.conn = sqlite3.connect(sql.db_path)
        self.cursor = self.conn.cursor()
        self.securedb = securesql.connect(sql.securedb_path)
        self.secure_cursor = self.securedb.cursor()

    table = ""

    # no init method needed
    def getTelemetry(self, norad_id: int, start_time: int = None, end_time: int = None, station: str = None, return_metadata: bool = False):
        telemetry = []
        # find data_type and set which table we are querying, using single quotes so sqlite doesn't get confused
        try:
            if norad_id != None:
                if start_time == None and end_time == None and station != None:
                    self.cursor.execute(f"""SELECT * FROM frames WHERE satellite={norad_id} AND station={station}""")
                    data = self.cursor.fetchall()
                    if return_metadata:
                        for i in range(len(data)):
                            telemetry.append([data[i][0], data[i][1], data[i][2], data[i][3]])
                    else:
                        for i in range(len(data)):
                            telemetry.append([data[i][1], data[i][2]])

                if start_time != None and end_time != None and station == None:
                    self.cursor.execute(f"""SELECT * FROM frames WHERE satellite={norad_id}""")
                    data = self.cursor.fetchall()
                    if return_metadata:
                        for i in range(len(data)):
                            if int(data[i][1]) >= start_time and int(data[i][1]) <= end_time:
                                telemetry.append([data[i][0], data[i][1], data[i][2], data[i][3]])
                    else:
                        for i in range(len(data)):
                            if int(data[i][1]) >= start_time and int(data[i][1]) <= end_time:
                                telemetry.append([data[i][1], data[i][2]])
                if start_time != None and end_time != None and station != None:
                    self.cursor.execute(f"""SELECT * FROM frames WHERE satellite={norad_id} AND station={station}""")
                    data = self.cursor.fetchall()
                    if return_metadata:
                        for i in range(len(data)):
                            if int(data[i][1]) >= start_time and int(data[i][1]) <= end_time:
                                telemetry.append([data[i][0], data[i][1], data[i][2], data[i][3]])
                    else:
                        for i in range(len(data)):
                            if int(data[i][1]) >= start_time and int(data[i][1]) <= end_time:
                                telemetry.append([data[i][1], data[i][2]])

                if start_time == None and end_time != None and station == None:
                    self.cursor.execute(f"""SELECT * FROM frames WHERE satellite={norad_id}""")
                    data = self.cursor.fetchall()
                    if return_metadata:
                        for i in range(len(data)):
                            if int(data[i][1]) <= end_time:
                                telemetry.append([data[i][0], data[i][1], data[i][2], data[i][3]])
                    else:
                        for i in range(len(data)):
                            if int(data[i][1]) <= end_time:
                                telemetry.append([data[i][1], data[i][2]])

                if start_time == None and end_time == None and station == None:
                    self.cursor.execute(f"""SELECT * FROM frames WHERE satellite={norad_id}""")
                    data = self.cursor.fetchall()
                    if return_metadata:
                        for i in range(len(data)):
                            telemetry.append([data[i][0], data[i][1], data[i][2], data[i][3]])
                    else:
                        for i in range(len(data)):
                            telemetry.append([data[i][1], data[i][2]])

                if start_time != None and end_time == None and station != None:
                    self.cursor.execute(f"""SELECT * FROM frames WHERE satellite={norad_id} AND station={station}""")
                    data = self.cursor.fetchall()
                    if return_metadata:
                        for i in range(len(data)):
                            if int(data[i][1]) >= start_time:
                                telemetry.append([data[i][0], data[i][1], data[i][2], data[i][3]])
                    else:
                        for i in range(len(data)):
                            if int(data[i][1]) >= start_time:
                                telemetry.append([data[i][1], data[i][2]])

                if start_time == None and end_time != None and station != None:
                    self.cursor.execute(f"""SELECT * FROM frames WHERE satellite={norad_id} AND station={station}""")
                    data = self.cursor.fetchall()
                    if return_metadata:
                        for i in range(len(data)):
                            if int(data[i][1]) <= end_time:
                                telemetry.append([data[i][0], data[i][1], data[i][2], data[i][3]])
                    else:
                        for i in range(len(data)):
                            if int(data[i][1]) <= end_time:
                                telemetry.append([data[i][1], data[i][2]])
                if start_time != None and end_time == None and station == None:
                    self.cursor.execute(f"""SELECT * FROM frames WHERE satellite={norad_id}""")
                    data = self.cursor.fetchall()
                    if return_metadata:
                        for i in range(len(data)):
                            if int(data[i][1]) >= start_time:
                                telemetry.append([data[i][0], data[i][1], data[i][2], data[i][3]])
                    else:
                        for i in range(len(data)):
                            if int(data[i][1]) >= start_time:
                                telemetry.append([data[i][1], data[i][2]])

            if norad_id == None:
                if start_time != None and end_time != None and station == None:
                    self.cursor.execute(f"""SELECT * FROM frames""")
                    data = self.cursor.fetchall()
                    if return_metadata:
                        for i in range(len(data)):
                            if int(data[i][1]) >= start_time and int(data[i][1]) <= end_time:
                                telemetry.append([data[i][0], data[i][1], data[i][2], data[i][3]])
                    else:
                        for i in range(len(data)):
                            if int(data[i][1]) >= start_time and int(data[i][1]) <= end_time:
                                telemetry.append([data[i][1], data[i][2]])

                if start_time == None and end_time == None and station != None:
                    self.cursor.execute(f"""SELECT * FROM frames WHERE station={station}""")
                    data = self.cursor.fetchall()
                    if return_metadata:
                        for i in range(len(data)):
                            telemetry.append([data[i][0], data[i][1], data[i][2], data[i][3]])
                    else:
                        for i in range(len(data)):
                            telemetry.append([data[i][1], data[i][2]])

                if start_time != None and end_time != None and station == None:
                    self.cursor.execute("""SELECT * FROM frames""")
                    data = self.cursor.fetchall()
                    if return_metadata:
                        for i in range(len(data)):
                            if int(data[i][1]) >= start_time and int(data[i][1]) <= end_time:
                                telemetry.append([data[i][0], data[i][1], data[i][2], data[i][3]])
                    else:
                        for i in range(len(data)):
                            if int(data[i][1]) >= start_time and int(data[i][1]) <= end_time:
                                telemetry.append([data[i][1], data[i][2]])
                if start_time != None and end_time != None and station != None:
                    self.cursor.execute(f"""SELECT * FROM frames WHERE station={station}""")
                    data = self.cursor.fetchall()
                    if return_metadata:
                        for i in range(len(data)):
                            if int(data[i][1]) >= start_time and int(data[i][1]) <= end_time:
                                telemetry.append([data[i][0], data[i][1], data[i][2], data[i][3]])
                    else:
                        for i in range(len(data)):
                            if int(data[i][1]) >= start_time and int(data[i][1]) <= end_time:
                                telemetry.append([data[i][1], data[i][2]])

                if start_time == None and end_time != None and station == None:
                    self.cursor.execute("""SELECT * FROM frames""")
                    data = self.cursor.fetchall()
                    if return_metadata:
                        for i in range(len(data)):
                            if int(data[i][1]) <= end_time:
                                telemetry.append([data[i][0], data[i][1], data[i][2], data[i][3]])
                    else:
                        for i in range(len(data)):
                            if int(data[i][1]) <= end_time:
                                telemetry.append([data[i][1], data[i][2]])

                if start_time == None and end_time == None and station == None:
                    self.cursor.execute("""SELECT * FROM frames""")
                    data = self.cursor.fetchall()
                    if return_metadata:
                        for i in range(len(data)):
                            telemetry.append([data[i][0], data[i][1], data[i][2], data[i][3]])
                    else:
                        for i in range(len(data)):
                            telemetry.append([data[i][1], data[i][2]])

                if start_time != None and end_time == None and station != None:
                    self.cursor.execute(f"""SELECT * FROM frames WHERE station={station}""")
                    data = self.cursor.fetchall()
                    if return_metadata:
                        for i in range(len(data)):
                            if int(data[i][1]) >= start_time:
                                telemetry.append([data[i][0], data[i][1], data[i][2], data[i][3]])
                    else:
                        for i in range(len(data)):
                            if int(data[i][1]) >= start_time:
                                telemetry.append([data[i][1], data[i][2]])

                if start_time == None and end_time != None and station != None:
                    self.cursor.execute(f"""SELECT * FROM frames WHERE station={station}""")
                    data = self.cursor.fetchall()
                    if return_metadata:
                        for i in range(len(data)):
                            if int(data[i][1]) <= end_time:
                                telemetry.append([data[i][0], data[i][1], data[i][2], data[i][3]])
                    else:
                        for i in range(len(data)):
                            if int(data[i][1]) <= end_time:
                                telemetry.append([data[i][1], data[i][2]])
                if start_time != None and end_time == None and station == None:
                    self.cursor.execute("""SELECT * FROM frames""")
                    data = self.cursor.fetchall()
                    if return_metadata:
                        for i in range(len(data)):
                            if int(data[i][1]) >= start_time:
                                telemetry.append([data[i][0], data[i][1], data[i][2], data[i][3]])
                    else:
                        for i in range(len(data)):
                            if int(data[i][1]) >= start_time:
                                telemetry.append([data[i][1], data[i][2]])
        except:
            telemetry = 1  # this will change when I assign actual db error numbers
        if telemetry != 1:
            if return_metadata:
                sorted(telemetry, key=operator.itemgetter(1))
            else:
                sorted(telemetry, key=operator.itemgetter(0))

            for i in range(len(telemetry)):
                if return_metadata:
                    telemetry[i][1] = datetime.datetime.utcfromtimestamp(telemetry[i][1]).strftime("%Y-%m-%d %H:%M:%S")
                else:
                    telemetry[i][0] = datetime.datetime.utcfromtimestamp(telemetry[i][0]).strftime("%Y-%m-%d %H:%M:%S")

        print(telemetry)
        return telemetry

    def getSatInfo(
        self,
        norad_id: int = None,
        name: str = None,
        deframer: str = None,
        country: str = None,
        return_all: bool = True,
        return_deframer: bool = False,
        return_launchinfo: bool = False,
        return_decoder: bool = False,
        return_name: bool = False,
        return_id: bool = False,
        return_description: bool = False,
    ):
        try:
            if norad_id != None and name == None and deframer == None and country == None:
                self.cursor.execute(f"""SELECT * FROM satellites WHERE norad_id={norad_id}""")
                data = self.cursor.fetchall()
            if name != None and norad_id == None and deframer == None and country == None:
                self.cursor.execute(f"""SELECT * FROM satellites WHERE name={name}""")
                data = self.cursor.fetchall()
            if name == None and norad_id == None and deframer != None and country == None:
                self.cursor.execute(f"""SELECT * FROM satellites WHERE deframer={deframer}""")
                data = self.cursor.fetchall()
            if name == None and norad_id == None and deframer == None and country != None:
                self.cursor.execute(f"""SELECT * FROM satellites WHERE country LIKE "%{country}%" """)
                data = self.cursor.fetchall()

            if return_all and not return_deframer and not return_launchinfo and not return_decoder and not return_name and not return_id and not return_description:
                info = []
                for i in range(len(data)):
                    info.append([data[i][0], data[i][1], data[i][2], data[i][3], data[i][4], data[i][5], data[i][6], data[i][7]])
                print(info)
            if return_deframer and not return_all and not return_launchinfo and not return_decoder and not return_name and not return_id and not return_description:
                info = []
                for i in range(len(data)):
                    info.append([data[i][5]])
                print(info)
            if return_launchinfo and not return_deframer and not return_all and not return_decoder and not return_name and not return_id and not return_description:
                info = []
                for i in range(len(data)):
                    info.append([data[i][3], data[i][4]])
                print(info)
            if return_decoder and not return_deframer and not return_all and not return_launchinfo and not return_name and not return_id and not return_description:
                info = []
                for i in range(len(data)):
                    info.append([data[i][6]])
                print(info)
            if return_name and not return_deframer and not return_all and not return_launchinfo and not return_decoder and not return_id and not return_description:
                info = []
                for i in range(len(data)):
                    info.append([data[i][1]])
                print(info)
            if return_id and not return_deframer and not return_all and not return_launchinfo and not return_decoder and not return_name and not return_description:
                info = []
                for i in range(len(data)):
                    info.append([data[i][0]])
                print(info)
            if return_description and not return_deframer and not return_all and not return_launchinfo and not return_decoder and not return_name and not return_id:
                info = []
                for i in range(len(data)):
                    info.append([data[i][2]])
                print(info)

        except ModuleNotFoundError:
            info = 1

    def appendTelemetry(self, norad_id: int, timestamps: list, frames: list, stations: list = [None]):
        if stations[0] == None:
            stations = []
            for i in range(len(timestamps) - 1):
                stations.append(None)

        print(stations)
        for i in range(len(frames) - 1):
            print(norad_id)
            print(timestamps[i])
            print(frames[i])
            print(stations[i])
            self.cursor.execute(
                """INSERT INTO telemetry (satellite, timestamp, frame, station) VALUES (?, ?, ?, ?)""",
                (int(norad_id), int(timestamps[i]), frames[i], str(stations[i])),
            )
            print(timestamps[i], frames[i], stations[i])

        self.conn.commit()

    def appendSatellite(
        self, norad_id: int, name: str, description: str = None, launch_date: str = None, deployment_date: str = None, deframer: str = None, decoder: str = None, countries: str = None
    ):
        # get rid of spaces
        self.cursor.execute(
            """INSERT INTO satellites (norad_id, name, description, launch_date, deployment_date, deframer, decoder, countries, in_orbit) VALUES (?, ?, ?, ?, ?, ?, ?, ?, 1)""",
            (norad_id, name, description, launch_date, deployment_date, deframer, decoder, countries),
        )
        print(norad_id, name, description, launch_date, deployment_date, decoder, countries)
        self.conn.commit()

    def notInOrbit(self, norad_id: int):
        self.cursor.execute(f"""UPDATE satellites SET in_orbit=0 WHERE norad_id={norad_id}""")

    def buildTelemetry(norad_id: int):
        print("clicking link\n")
        webbot.clicker(norad_id)
        print("fetching link\n")
        link = mail.fetch(env_vars.mail_user, env_vars.mail_passwd)
        print("downloading csv\n")
        mail.download(link, norad_id)
        print("reading csv\n")
        timestamps, frames = readCSV(norad_id)
        print(timestamps)
        print("done reading\n")
        print("appending to sql db\n")
        sql().appendTelemetry(norad_id=norad_id, timestamps=timestamps, frames=frames)
        print("finished")

    def buildSatInfo(self, norad_id: int):
        decoders = [None]
        deframers = [None]
        url = f"https://db-dev.satnogs.org/api/satellites/?norad_cat_id={norad_id}"
        response = requests.get(url=url, headers={"Authorization": "Tokenc06f6fc8a880500669aa18a8ef2743cc4acc1e1d"})
        data = response.json()[0]
        description = f"User Entry: {input('Enter a description for the satellite: ')} \n\n Website: {data['website']}"
        if data["launched"] == None:
            if input("Do you want to manually enter a launch date? (y/n) ").strip().lower() == "y":
                launch_date = input("Enter a launch date (YYYY-MM-DDTHH:MM:SSZ): ")
            else:
                launch_date = None
        else:
            launch_date = data["launched"]
        if data["deployed"] == None:
            if input("Do you want to manually enter a deployment date? (y/n) ").strip().lower() == "y":
                deployment_date = input("Enter a deployment date (YYYY-MM-DDTHH:MM:SSZ): ")
            else:
                deployment_date = None
        else:
            deployment_date = data["deployed"]
        done = True
        while done:
            try:
                for i in range(len(deframers)):
                    print(f"{i+1}: {deframers[i]}")
                deframer = deframers[int(input("Choose a deframer: ")) - 1]
                done = False
            except:
                print("Enter the number corresponding to the option you want")
        done = True
        while done:
            try:
                for i in range(len(decoders)):
                    print(f"{i+1}: {decoders[i]}")
                decoder = decoders[int(input("Choose a decoder: ")) - 1]
                done = False
            except:
                print("Enter the number corresponding to the option you want")

        sql().appendSatellite(
            norad_id=norad_id, description=description, launch_date=launch_date, deployment_date=deployment_date, deframer=deframer, decoder=decoder, countries=data["countries"], name=data["name"]
        )

    def getUserInfo(self, key, username, password, all_data: bool = False, email_login: bool = False, tracker_info: bool = False, satnogs_key: bool = False, is_admin: bool = False):
        if key == None:
            print("Database encryption key was not passed.")
            quit
        try:
            self.secure_cursor.executescript(
                f"""PRAGMA key='{key}';
                    PRAGMA cipher_compatibility = 3"""
            )
        except:
            print("Database key is incorrect.")
            quit
        if username == None or password == None:
            print("Either the username or password was not passed.")
            quit

        if all_data and not email_login and not tracker_info and not is_admin and not satnogs_key:
            self.secure_cursor.execute(f"""select lat, lng, email, email_passwd, satnogs_key, ny2o_key, admin from info where username={username} and password={password}""")
            data = self.secure_cursor.fetchall()
            info = [data[0][0], data[0][1], data[0][2], data[0][3], data[0][4], data[0][5], data[0][6]]
        if not all_data and email_login and not tracker_info and not is_admin and not satnogs_key:
            self.secure_cursor.execute(f"""select email, email_passwd from info where username={username} and password={password}""")
            data = self.secure_cursor.fetchall()
            info = [data[0][0], data[0][1]]
        if not all_data and not email_login and tracker_info and not is_admin and not satnogs_key:
            self.secure_cursor.execute(f"""select lat, lng, ny2o_key from info where username='{username}' and password='{password}'""")
            data = self.secure_cursor.fetchall()
            info = [data[0][0], data[0][1], data[0][2]]
        if not all_data and not email_login and not tracker_info and not is_admin and satnogs_key:
            self.secure_cursor.execute(f"""select lat, lng, ny2o_key from info where username='{username}' and password='{password}'""")
            data = self.secure_cursor.fetchall()
            info = [data[0][0]]
        if all_data and not email_login and not tracker_info and is_admin and not satnogs_key:
            self.secure_cursor.execute(f"""select admin from info where username={username} and password={password}""")
            if self.secure_cursor.fetchall()[0][0] == 1:
                info = True
            else:
                info = False

        return info

    def buildUserInfo(self):
        pass

    def __del__(self):
        self.conn.close()


# anything beyond this point is for testing

# print(timestamps)
# print(frames)

"""
"""
"""
sql().appendTelemetry(
    norad_id=25544,
    timestamps=[1700859867, 1700859868, 1700859869, 1700859870, 1700859871, 1700859872, 1700859873, 1700859874],
    frames=[
        "60A060A0A66C609C8262A6A640E082A0A4A682A86103F02776261C6C201C53495D41524953532D49535320504D323D0D",
        "60A060A0A66C609C8262A6A640E082A0A4A682A86103F02776261C6C201C53495D41524953532D49535320504D323D0D",
        "60A060A0A66C609C8262A6A640E082A0A4A682A86103F02776261C6C201C53495D41524953532D49535320504D323D0D",
        "60A060A0A66C609C8262A6A640E082A0A4A682A86103F02776261C6C201C53495D41524953532D49535320504D323D0D",
        "60A060A0A66C609C8262A6A640E082A0A4A682A86103F02776261C6C201C53495D41524953532D49535320504D323D0D",
        "60A060A0A66C609C8262A6A640E082A0A4A682A86103F02776261C6C201C53495D41524953532D49535320504D323D0D",
        "60A060A0A66C609C8262A6A640E082A0A4A682A86103F02776261C6C201C53495D41524953532D49535320504D323D0D",
        "60A060A0A66C609C8262A6A640E082A0A4A682A86103F02776261C6C201C53495D41524953532D49535320504D323D0D",
    ],
    stations=["plat0-3a-EN61cn", "9V1KG-OJ11xi", "M0EYT / 2E0NOG-IO80xs", "M0EYT / 2E0NOG-IO80xs", "M0EYT / 2E0NOG-IO80xs", "M0EYT / 2E0NOG-IO80xs", "M0EYT / 2E0NOG-IO80xs", "M0EYT / 2E0NOG-IO80xs"],
)

sql().appendSatellite(
    norad_id=25544,
    name="ISS",
    description="The International Space Station is a partnership between the US and Russia. It is made of mutiple modules, and houses astronauts from multiple countries",
    countries="US, Ru",
)
"""


"""
# cursor.get(1693464165, 1693541620)


# cursor.get(1530633289, 1688256077)
# cursor.append("", 96.42)


# conn = sqlite3.connect(f"dbs/{norad_id}.db")
# c = conn.cursor()
"""
