import time
import initalize
import sqlite3

conn = sqlite3.connect("data.db")
c = conn.cursor()

def parse(data):
        unparsed_data = str(data)
        final_data = 0
        
        step1 = unparsed_data.replace("[", "")
        step2 = step1.replace("(", "")
        step3 = step2.replace(")", "")
        final_data = step3.replace("]", "")
        if final_data == "":
            final_data = "0,"
        return final_data

class sql:


    table = ""
    #no init method needed
    def get(self, start_time, end_time, data_type):
        y_list =  ""
        data_type = data_type.replace(" ", "")
        #find data_type and set which table we are querying, using single quotes so sqlite doesn't get confused
        if data_type.lower() == "temp":
            while start_time <= end_time:
                #convert into str because sqlite is picky like that
                str_time = "%s" % start_time
                c.execute("""SELECT data FROM temp WHERE unix_time = ?""", [str_time])
                data = c.fetchall()
                y_list += str(parse(data))
                print(y_list)
                start_time+=1
                

        if data_type.lower() == "altitude":
            while start_time <= end_time:
                #convert into str because sqlite is picky like that
                str_time = "%s" % start_time
                c.execute("""SELECT data FROM altitude WHERE unix_time = ?""", [str_time])
                data = c.fetchall()
                y_list += str(parse(data))
                print(y_list)
                start_time+=1

        if data_type.lower() == "airpressure":
            while start_time <= end_time:
                #convert into str because sqlite is picky like that
                str_time = "%s" % start_time
                c.execute("""SELECT data FROM airpressure WHERE unix_time = ?""", [str_time])
                data = c.fetchall()
                y_list += str(parse(data))
                print(y_list)
                start_time+=1

        if data_type == "gps":
            while start_time <= end_time:
                #convert into str because sqlite is picky like that
                str_time = "%s" % start_time
                c.execute("""SELECT data FROM gps WHERE unix_time = ?""", [str_time])
                data = c.fetchall()
                y_list += str(parse(data))
                print(y_list)
                start_time+=1

        #remove extra comma
        y_list = y_list[:-1]
        return y_list      

    def append(self, data_type, data):
        #callable names
        supported_names= "tempaltitudeairpressuregpsimagepicturetemperature"
        #get rid of spaces
        data_type = data_type.replace(" ", "")
        if data_type.lower() == "temp":
            c.execute("""INSERT INTO temp VALUES (?, ?)""", (round(time.time()), data))
        if data_type.lower() == "altitude":
            c.execute("""INSERT INTO altitude VALUES (?, ?)""", (round(time.time()), data))
        if data_type.lower() == "airpressure" or data_type.lower() == "air pressure":
            c.execute("""INSERT INTO temp VALUES (?, ?)""", (round(time.time()), data))
        if data_type.lower() == "gps" :
            c.execute("""INSERT INTO gps VALUES (?, ?)""", (round(time.time()), data))
        #fix this later
        if data_type.lower() == "image" or data_type.lower() == "pictures":
            c.execute("""INSERT INTO  images VALUES (?, ?)""", (round(time.time()), data))
        #support for one unsupported data type per db in the form of the "other" collom
        if data_type not in supported_names:
            c.execute("""INSERT INTO other VALUES (?, ?)""", (round(time.time()), data))
        else:
            print("[Data type not in DB]")
            conn.commit()



console = sql()
#console.get(1685335865, 1685335870, "temp")
console.append("", 96.42)
#c.execute("SELECT * FROM temp")
#print(c.fetchall())
