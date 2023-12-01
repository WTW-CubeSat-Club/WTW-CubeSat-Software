import time
import sqlite3
import os
import csv
import calendar
import mail
import webbot
import env_vars
import os
import datetime
import operator

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

    return norad_id, timestamps, frames


class sql:
    db_folder = "data"
    db_name = "data"
    db_path = f"{script_dir}/{db_folder}/{db_name}.db"

    def __init__(self):
        self.conn = sqlite3.connect(sql.db_path)
        self.cursor = self.conn.cursor()

    table = ""

    # no init method needed
    def getTelemetry(self, norad_id: int, start_time: int = None, end_time: int = None, station_id: str = None, return_metadata: bool = False):
        telemetry = []
        # find data_type and set which table we are querying, using single quotes so sqlite doesn't get confused
        try:
            if norad_id != None:
                if start_time == None and end_time == None and station_id != None:
                    self.cursor.execute(f"""SELECT * FROM frames WHERE satellite={norad_id} AND station_id={station_id}""")
                    data = self.cursor.fetchall()
                    if return_metadata:
                        for i in range(len(data) - 1):
                            telemetry.append([data[i][0], data[i][1], data[i][2], data[i][3]])
                    else:
                        for i in range(len(data) - 1):
                            telemetry.append([data[i][1], data[i][2]])

                if start_time != None and end_time != None and station_id == None:
                    self.cursor.execute(f"""SELECT * FROM frames WHERE satellite={norad_id}""")
                    data = self.cursor.fetchall()
                    if return_metadata:
                        for i in range(len(data) - 1):
                            if int(data[i][1]) >= start_time and int(data[i][1]) <= end_time:
                                telemetry.append([data[i][0], data[i][1], data[i][2], data[i][3]])
                    else:
                        for i in range(len(data) - 1):
                            if int(data[i][1]) >= start_time and int(data[i][1]) <= end_time:
                                telemetry.append([data[i][1], data[i][2]])
                if start_time != None and end_time != None and station_id != None:
                    self.cursor.execute(f"""SELECT * FROM frames WHERE satellite={norad_id} AND station_id={station_id}""")
                    data = self.cursor.fetchall()
                    if return_metadata:
                        for i in range(len(data) - 1):
                            if int(data[i][1]) >= start_time and int(data[i][1]) <= end_time:
                                telemetry.append([data[i][0], data[i][1], data[i][2], data[i][3]])
                    else:
                        for i in range(len(data) - 1):
                            if int(data[i][1]) >= start_time and int(data[i][1]) <= end_time:
                                telemetry.append([data[i][1], data[i][2]])

                if start_time == None and end_time != None and station_id == None:
                    self.cursor.execute(f"""SELECT * FROM frames WHERE satellite={norad_id}""")
                    data = self.cursor.fetchall()
                    if return_metadata:
                        for i in range(len(data) - 1):
                            if int(data[i][1]) <= end_time:
                                telemetry.append([data[i][0], data[i][1], data[i][2], data[i][3]])
                    else:
                        for i in range(len(data) - 1):
                            if int(data[i][1]) <= end_time:
                                telemetry.append([data[i][1], data[i][2]])

                if start_time == None and end_time == None and station_id == None:
                    self.cursor.execute(f"""SELECT * FROM frames WHERE satellite={norad_id}""")
                    data = self.cursor.fetchall()
                    if return_metadata:
                        for i in range(len(data) - 1):
                            telemetry.append([data[i][0], data[i][1], data[i][2], data[i][3]])
                    else:
                        for i in range(len(data) - 1):
                            telemetry.append([data[i][1], data[i][2]])

                if start_time != None and end_time == None and station_id != None:
                    self.cursor.execute(f"""SELECT * FROM frames WHERE satellite={norad_id} AND station_id={station_id}""")
                    data = self.cursor.fetchall()
                    if return_metadata:
                        for i in range(len(data) - 1):
                            if int(data[i][1]) >= start_time:
                                telemetry.append([data[i][0], data[i][1], data[i][2], data[i][3]])
                    else:
                        for i in range(len(data) - 1):
                            if int(data[i][1]) >= start_time:
                                telemetry.append([data[i][1], data[i][2]])

                if start_time == None and end_time != None and station_id != None:
                    self.cursor.execute(f"""SELECT * FROM frames WHERE satellite={norad_id} AND station_id={station_id}""")
                    data = self.cursor.fetchall()
                    if return_metadata:
                        for i in range(len(data) - 1):
                            if int(data[i][1]) <= end_time:
                                telemetry.append([data[i][0], data[i][1], data[i][2], data[i][3]])
                    else:
                        for i in range(len(data) - 1):
                            if int(data[i][1]) <= end_time:
                                telemetry.append([data[i][1], data[i][2]])
                if start_time != None and end_time == None and station_id == None:
                    self.cursor.execute(f"""SELECT * FROM frames WHERE satellite={norad_id}""")
                    data = self.cursor.fetchall()
                    if return_metadata:
                        for i in range(len(data) - 1):
                            if int(data[i][1]) >= start_time:
                                telemetry.append([data[i][0], data[i][1], data[i][2], data[i][3]])
                    else:
                        for i in range(len(data) - 1):
                            if int(data[i][1]) >= start_time:
                                telemetry.append([data[i][1], data[i][2]])

            if norad_id == None:
                if start_time != None and end_time != None and station_id == None:
                    self.cursor.execute(f"""SELECT * FROM frames""")
                    data = self.cursor.fetchall()
                    if return_metadata:
                        for i in range(len(data) - 1):
                            if int(data[i][1]) >= start_time and int(data[i][1]) <= end_time:
                                telemetry.append([data[i][0], data[i][1], data[i][2], data[i][3]])
                    else:
                        for i in range(len(data) - 1):
                            if int(data[i][1]) >= start_time and int(data[i][1]) <= end_time:
                                telemetry.append([data[i][1], data[i][2]])

                if start_time == None and end_time == None and station_id != None:
                    self.cursor.execute(f"""SELECT * FROM frames WHERE station_id={station_id}""")
                    data = self.cursor.fetchall()
                    if return_metadata:
                        for i in range(len(data) - 1):
                            telemetry.append([data[i][0], data[i][1], data[i][2], data[i][3]])
                    else:
                        for i in range(len(data) - 1):
                            telemetry.append([data[i][1], data[i][2]])

                if start_time != None and end_time != None and station_id == None:
                    self.cursor.execute("""SELECT * FROM frames""")
                    data = self.cursor.fetchall()
                    if return_metadata:
                        for i in range(len(data) - 1):
                            if int(data[i][1]) >= start_time and int(data[i][1]) <= end_time:
                                telemetry.append([data[i][0], data[i][1], data[i][2], data[i][3]])
                    else:
                        for i in range(len(data) - 1):
                            if int(data[i][1]) >= start_time and int(data[i][1]) <= end_time:
                                telemetry.append([data[i][1], data[i][2]])
                if start_time != None and end_time != None and station_id != None:
                    self.cursor.execute(f"""SELECT * FROM frames WHERE station_id={station_id}""")
                    data = self.cursor.fetchall()
                    if return_metadata:
                        for i in range(len(data) - 1):
                            if int(data[i][1]) >= start_time and int(data[i][1]) <= end_time:
                                telemetry.append([data[i][0], data[i][1], data[i][2], data[i][3]])
                    else:
                        for i in range(len(data) - 1):
                            if int(data[i][1]) >= start_time and int(data[i][1]) <= end_time:
                                telemetry.append([data[i][1], data[i][2]])

                if start_time == None and end_time != None and station_id == None:
                    self.cursor.execute("""SELECT * FROM frames""")
                    data = self.cursor.fetchall()
                    if return_metadata:
                        for i in range(len(data) - 1):
                            if int(data[i][1]) <= end_time:
                                telemetry.append([data[i][0], data[i][1], data[i][2], data[i][3]])
                    else:
                        for i in range(len(data) - 1):
                            if int(data[i][1]) <= end_time:
                                telemetry.append([data[i][1], data[i][2]])

                if start_time == None and end_time == None and station_id == None:
                    self.cursor.execute("""SELECT * FROM frames""")
                    data = self.cursor.fetchall()
                    if return_metadata:
                        for i in range(len(data) - 1):
                            telemetry.append([data[i][0], data[i][1], data[i][2], data[i][3]])
                    else:
                        for i in range(len(data) - 1):
                            telemetry.append([data[i][1], data[i][2]])

                if start_time != None and end_time == None and station_id != None:
                    self.cursor.execute(f"""SELECT * FROM frames WHERE station_id={station_id}""")
                    data = self.cursor.fetchall()
                    if return_metadata:
                        for i in range(len(data) - 1):
                            if int(data[i][1]) >= start_time:
                                telemetry.append([data[i][0], data[i][1], data[i][2], data[i][3]])
                    else:
                        for i in range(len(data) - 1):
                            if int(data[i][1]) >= start_time:
                                telemetry.append([data[i][1], data[i][2]])

                if start_time == None and end_time != None and station_id != None:
                    self.cursor.execute(f"""SELECT * FROM frames WHERE station_id={station_id}""")
                    data = self.cursor.fetchall()
                    if return_metadata:
                        for i in range(len(data) - 1):
                            if int(data[i][1]) <= end_time:
                                telemetry.append([data[i][0], data[i][1], data[i][2], data[i][3]])
                    else:
                        for i in range(len(data) - 1):
                            if int(data[i][1]) <= end_time:
                                telemetry.append([data[i][1], data[i][2]])
                if start_time != None and end_time == None and station_id == None:
                    self.cursor.execute("""SELECT * FROM frames""")
                    data = self.cursor.fetchall()
                    if return_metadata:
                        for i in range(len(data) - 1):
                            if int(data[i][1]) >= start_time:
                                telemetry.append([data[i][0], data[i][1], data[i][2], data[i][3]])
                    else:
                        for i in range(len(data) - 1):
                            if int(data[i][1]) >= start_time:
                                telemetry.append([data[i][1], data[i][2]])
        except:
            telemetry = [[1]]  # this will change when I assign actual db error numbers

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
            info = [[1]]

    def appendTelemetry(self, norad_id: int, timestamps: list, frames: list, station_ids: list = [None]):
        if station_ids[0] == None:
            station_ids = []
            for i in range(len(timestamps) - 1):
                station_ids.append(None)

        for i in range(len(frames) - 1):
            self.cursor.execute(
                """INSERT INTO frames (satellite, timestamp, data, station_id) VALUES (?, ?, ?, ?)""",
                (norad_id, timestamps[i], frames[i], station_ids[i]),
            )
            print(timestamps[i], frames[i], station_ids[i])

        self.conn.commit()

    def appendSatellite(
        self, norad_id: int, name: str, description: str = None, launch_date: str = None, deployment_date: str = None, deframer: str = None, decoder: str = None, countries: str = None
    ):
        # get rid of spaces
        self.cursor.execute(
            """INSERT INTO satellites (norad_id, name, description, launch_date, deployment_date, deframer, decoder, countries) VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (norad_id, name, description, launch_date, deployment_date, deframer, decoder, countries),
        )
        print(norad_id, name, description, launch_date, deployment_date, decoder, countries)
        self.conn.commit()

    def createDB(self):
        self.cursor.executescript(  # maybe remove timestamp in frame cuz its duplicate data
            """
            DROP TABLE IF EXISTS frames;

            CREATE TABLE IF NOT EXISTS frames (
                satellite integer,
                timestamp integer,
                data blob,
                station_id string
                );

            DROP TABLE IF EXISTS satellites;
            
            CREATE TABLE IF NOT EXISTS satellites (
                norad_id integer,
                name string,
                description string,
                launch_date string,
                deployment_date string,
                deframer string,
                decoder string,
                countries string
                )
        """
        )

        self.conn.commit()

    def migrate(self):
        self.createDB()

    def __del__(self):
        self.conn.close()


def DBCheck(norad_id: int):
    # change to recieve input from client
    user_input = input(f"Do you want to fetch all data for satellite {norad_id}")
    if user_input.lower() == "y":
        print("clicking link\n")
        webbot.clicker(norad_id)
        print("fetching link\n")
        link = mail.fetch(env_vars.mail_user, env_vars.mail_passwd)
        print("downloading csv\n")
        mail.download(link, norad_id)
        print("reading csv\n")
        norad_ids, timestamps, frames = readCSV(norad_id)
        print(timestamps)
        print("done reading\n")
        print("appending to sql db\n")
        cursor = sql(norad_id)
        cursor.appendTelemetry(norad_id=norad_ids, timestamps=timestamps, frames=frames)
        print("finished")


DBCheck(40910)


# anything beyond this point is for testing

# print(timestamps)
# print(frames)

"""

"""

# cursor.get(1693464165, 1693541620)


# cursor.get(1530633289, 1688256077)
# cursor.append("", 96.42)


# conn = sqlite3.connect(f"dbs/{norad_id}.db")
# c = conn.cursor()
