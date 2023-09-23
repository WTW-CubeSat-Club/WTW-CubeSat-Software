import time
import sqlite3
import os
import csv
import calendar
import mail
import webbot
import env_vars
import os

norad_id = 41619
script_dir = env_vars.script_dir

#read downloaded csv cache
def readCSV(norad_id:int):
    timestamps_raw = []
    frames_raw = []
    timestamps = []
    frames = []
    # opening the CSV file
    with open(f"{script_dir}csv_cache/{norad_id}data.csv", mode ='r')as file:
        # reading the CSV file
        csvFile = csv.reader(file)

        # displaying the contents of the CSV file
        for line in csvFile:
            str_line = line[0]
            split_line = str_line.split("|")
            timestamp = str(calendar.timegm(time.strptime(split_line[0], '%Y-%m-%d %H:%M:%S')))
            timestamps_raw.append(timestamp)
            frames_raw.append(split_line[1])
        #remove duplicates
        for i in range(len(frames_raw)-1):
            if frames_raw[i] not in frames:
                frames.append(frames_raw[i])
                timestamps.append(timestamps_raw[i])
    print(len(timestamps_raw))
    print(len(timestamps))
    #reverse lists to it can go from end time to start time
    timestamps.reverse()
    frames.reverse()
    os.remove(f"{script_dir}csv_cache/{norad_id}data.csv")
        
    return timestamps, frames





#this is a text function that imitates requests from server.py
#checks if database exists, if not creates database and populates it with csv cache
#path to dbs will change depending on which folder you run the script in in vscode

has_satellite = os.path.exists(f"{script_dir}/dbs/{norad_id}.db")
if not has_satellite:
    create_db = input("Do you want to create a new database? ")
    if create_db.lower() == "y":
        conn = sqlite3.connect(f"{script_dir}/dbs/{norad_id}.db")
        c = conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS data (
            unix_time integer,
            data blob
        )""")
    
        print("clicking link\n")
        webbot.clicker(norad_id)
        print("fetching link\n")
        link = mail.fetch(env_vars.mail_user, env_vars.mail_passwd)
        print("downloading csv\n")
        file = mail.download(link, norad_id)

        #path to cache will change depending on which folder you run the script in in vscode
        print("reading csv\n")

        timestamps, frames = readCSV(norad_id)
        print(timestamps)
        print("done reading\n")

        







class sql:

    def __init__(self, norad_id:int):
        self.norad_id = str(norad_id)
        self.conn = sqlite3.connect(f"{script_dir}/dbs/{norad_id}.db")
        self.c = self.conn.cursor()

    table = ""
    #no init method needed
    def get(self, start_time:int, end_time:int):
        y_list =  []
        #find data_type and set which table we are querying, using single quotes so sqlite doesn't get confused
        self.c.execute("""SELECT * FROM data""")
        data = self.c.fetchall()
        for i in range(len(data)-1):
            if int(data[i][0]) >= start_time and int(data[i][0]) <= end_time:
                y_list.append(data[i][1])

    
        print(y_list)
        return y_list      

    def append(self, timestamps:list, frames:list):
        #get rid of spaces
        for i in range(len(frames)-1):
            self.c.execute("""INSERT INTO data VALUES (?, ?)""", (timestamps[i], frames[i]))
            print(timestamps[i],frames[i])
    
        self.conn.commit()

    
#anything beyond this point is for testing

#print(timestamps)
#print(frames)
"""
console = sql(norad_id)
if not has_satellite:
    print("appending to sql db\n")
    console.append(timestamps, frames)
    print("finished")
"""

#console.get(1693464165, 1693541620)


#console.get(1530633289, 1688256077)
#console.append("", 96.42)


#conn = sqlite3.connect(f"dbs/{norad_id}.db")
#c = conn.cursor()
