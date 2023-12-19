import sqlite3
import env_vars
from pysqlcipher3 import dbapi2 as securesql
import getpass
import os

script_dir = env_vars.script_dir


class sql:
    db_folder = "data"
    db_name = "data"
    secure_db_name = "private"
    db_path = f"{script_dir}/{db_folder}/{db_name}.db"
    secure_db_path = f"{script_dir}/{db_folder}/{secure_db_name}.db"
    print(secure_db_path)

    table = ""

    def createSecureDB(self):
        if os.path.exists(sql.secure_db_path):
            os.remove(sql.secure_db_path)
        self.securedb = securesql.connect(sql.secure_db_path)
        self.secure_cursor = self.securedb.cursor()
        key = getpass.getpass("Enter the key that will be used to encrypt the user database: ")
        self.secure_cursor.executescript(
            f"""
            PRAGMA key = '{key}';

            PRAGMA cipher_compatibility = 3;

            create table if not exists info (
                username str,
                password str,
                lat real,
                lng real,
                email str,
                email_passwd str,
                satnogs_key str,
                ny2o_key str,
                is_admin int
            )
            """
        )

    def createDB(self):
        self.conn = sqlite3.connect(sql.db_path)
        self.cursor = self.conn.cursor()
        self.cursor.executescript(
            """
            DROP TABLE IF EXISTS frames;

            CREATE TABLE IF NOT EXISTS telemetry (
                satellite integer,
                timestamp integer,
                frame blob,
                station string
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
                countries string,
                in_orbit int
                )
        """
        )

        self.conn.commit()

    def migrate(self):
        self.createSecureDB()
        # self.createDB()

    def __del__(self):
        self.conn.close()
        self.securedb.close()


if __name__ == "__main__":
    if input("Are you sure you want to delete the database and recreate it? (y/n) ").strip() == "y":
        sql().migrate()

# Checklist

# fix SQL get and append
# change DBCheck and update_frames to work with new DB system
# HI POOKIE DOOKIE BOOKIE BEAR
