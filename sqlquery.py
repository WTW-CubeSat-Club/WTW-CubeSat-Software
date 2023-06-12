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
        #find data_type and set which table we are querying, using single quotes so sqlite doesn't get confused
        if data_type == "temp":
            while start_time <= end_time:
                #convert into str because sqlite is picky like that
                str_time = "%s" % start_time
                c.execute("""SELECT data FROM temp WHERE unix_time = ?""", [str_time])
                data = c.fetchall()
                y_list += str(parse(data))
                print(y_list)
                start_time+=1
                

        if data_type == "altitude":
            while start_time <= end_time:
                #convert into str because sqlite is picky like that
                str_time = "%s" % start_time
                c.execute("""SELECT data FROM altitude WHERE unix_time = ?""", [str_time])
                data = c.fetchall()
                y_list += str(parse(data))
                print(y_list)
                start_time+=1

        #remove extra comma
        y_list = y_list[:-1]
        return y_list      

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



#console = sql()
#console.get(1685335865, 1685335870, "temp")
#console.append("temp", 96.42)
#c.execute("SELECT * FROM temp")
#print(c.fetchall())
