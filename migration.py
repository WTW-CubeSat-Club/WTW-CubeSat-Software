import sqlite3
import env_vars

script_dir = env_vars.script_dir


class sql:
    db_folder = "data"
    db_name = "data"
    db_path = f"{script_dir}/{db_folder}/{db_name}.db"

    def __init__(self):
        self.conn = sqlite3.connect(sql.db_path)
        self.cursor = self.conn.cursor()

    table = ""

    def createDB(self):
        self.cursor.executescript(
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


if __name__ == "__main__":
    if input("Are you sure you want to delete the database and recreate it? (y/n) ").strip() == "y":
        sql.migrate()

# Checklist

# fix SQL get and append
# change DBCheck and update_frames to work with new DB system
