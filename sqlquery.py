import sqlite3
import time

#takes unix time and rounds to get an int
#unix_time =  round(time.time())
conn = sqlite3.connect("data.db")
#data_value = 97


#create cursor
c = conn.cursor()


#? represents variable values
#c.execute("INSERT INTO temp VALUES (?, ?)", (unix_time, data_value))

#c.execute("SELECT * FROM temp")
#print(c.fetchall())

#commit
#conn.commit()

#close
#conn.close()

class sql:

    table = ""
    #no init method needed
    def get(self, start_time, end_time, data_type):
        data_list =  ""
        #find data_type and set which table we are querying, using single quotes so sqlite doesn't get confused
        if data_type == "temp":
            while start_time <= end_time:
                #convert into str because sqlite is picky like that
                str_time = "%s" % start_time
                print(str_time)
                c.execute("""SELECT unix_time, data FROM temp WHERE unix_time = ?""", [str_time])
                data = c.fetchall()
                datastr = f"{str_time}\n{str(data)}\n"
                start_time+=1
                print(datastr)
                data_list+=datastr

        if data_type == "altitude":
            while start_time <= end_time:
                #convert into str because sqlite is picky like that
                str_time = "%s" % start_time
                c.execute("""SELECT * FROM altitude WHERE unix_time = ?""", [str_time])
                data = c.fetchall()
                datastr = f"{str_time}\n{str(data)}\n"
                print(datastr)
                start_time+=1
                print(data)
                data_list+=datastr

        return data_list        

    def append(self, data_type, data):
        #using if statements so I don't have to interpolate the data_type
        if data_type == "temp":
            c.execute("""INSERT INTO temp VALUES (?, ?)""", (round(time.time()), data))
        if data_type == "altitude":
            c.execute("""INSERT INTO altitude VALUES (?, ?)""", (round(time.time()), data))
        if data_type == "airpressure":
            c.execute("""INSERT INTO temp VALUES (?, ?)""", (round(time.time()), data))
        """  else:
            print("Invalid data type")
        """
        conn.commit()
"""
console = sql()
console.get(1685335865, 1685335870, "temp")
console.append("temp", 96.42)
c.execute("SELECT * FROM temp")
print(c.fetchall())

#conn.close()"""