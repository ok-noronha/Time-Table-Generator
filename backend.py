import psycopg2
import sys
from psycopg2 import connect
from psycopg2 import OperationalError, errorcodes, errors


class DataBase:
    def __init__(self, usrid, password):
        self.usrid = usrid
        self.password = password

    def connect_db(self):
        return psycopg2.connect(
            user="postgres",
            password="1024",
            host="localhost",
            port="5432",
            database="ttdb",
        )

    def create_cur(self, conn):
        return (conn.cursor(), conn)

    def add_course(self, code, hours, cur=None):
        if cur is None:
            cur = self.create_cur(self.connect_db())
        try:
            cur[0].execute(f"INSERT INTO courses VALUES ( '{code}',{hours},{self.usrid})")
            cur[1].commit()
            return True
        except Exception as error:
            print ("Oops! An exception has occured:", error)
            print ("Exception TYPE:", type(error))
            return False

    def get_courses(self, code, cur=None):
        if cur is None:
            cur = self.create_cur(self.connect_db())
        try:
            cur[0].execute(f"SELECT * FROM courses WHERE code='{code}' AND usrid={self.usrid};")
            return cur[0].fetchone()
        except Exception as error:
            print ("Oops! An exception has occured:", error)
            print ("Exception TYPE:", type(error))
            print("course code not found")
            return None

    def delete_course(self, code, cur=None):
        if cur is None:
            cur = self.create_cur(self.connect_db())
        try:
            cur[0].execute(f"DELETE FROM courses WHERE code='{code}'AND usrid={self.usrid};")
            cur[0].execute(f"DELETE FROM courses_cpy WHERE code='{code}'AND usrid={self.usrid};")
            cur[1].commit()
            return True
        except Exception as error:
            print ("Oops! An exception has occured:", error)
            print ("Exception TYPE:", type(error))
            print("course not deleted")
            return False

    def time_table(self, cur=None):
        if cur is None:
            cur = self.create_cur(self.connect_db())
        try:
            cur[0].execute(
                """UPDATE jobs
            SET code = 'LUNCH'
            WHERE hour=15 OR hour=25 OR hour=35 OR hour=45 OR hour=55"""
            )
            cur[1].commit()
            return True
        except Exception as error:
            print ("Oops! An exception has occured:", error)
            print ("Exception TYPE:", type(error))
            print("The time-table is not computed")
            return False

    def get_jobs(self, cur=None):
        if cur is None:
            cur = self.create_cur(self.connect_db())
        try:
            cur[0].execute(f"SELECT * FROM jobs WHERE usrid={self.usrid};")
            return cur[0].fetchall()
        except Exception as error:
            print ("Oops! An exception has occured:", error)
            print ("Exception TYPE:", type(error))
            print("Cant extract time table")
            return None

    def create_user(self, cur=None):
        if cur is None:
            cur = self.create_cur(self.connect_db())
        try:
            print(type(self.usrid))
            print(self.usrid)
            ids = self.usrid
            pswd= self.password
            cur[0].execute(
                f"INSERT INTO authentication VALUES ({ids},{pswd});")
            print(type(self.usrid))
            cur[0].execute(
                f"INSERT INTO jobs (hour,usrid) VALUES (11,{self.usrid}),(12,{self.usrid}),(13,{self.usrid}),(14,{self.usrid}),(15,{self.usrid}),(16,{self.usrid}),(17,{self.usrid}),(21,{self.usrid}),(22,{self.usrid}),(23,{self.usrid}),(24,{self.usrid}),(25,{self.usrid}),(26,{self.usrid}),(27,{self.usrid}),(31,{self.usrid}),(32,{self.usrid}),(33,{self.usrid}),(34,{self.usrid}),(35,{self.usrid}),(36,{self.usrid}),(37,{self.usrid}),(41,{self.usrid}),(42,{self.usrid}),(43,{self.usrid}),(44,{self.usrid}),(45,{self.usrid}),(46,{self.usrid}),(47,{self.usrid}),(51,{self.usrid}),(52,{self.usrid}),(53,{self.usrid}),(54,{self.usrid}),(55,{self.usrid}),(56,{self.usrid}),(57,{self.usrid}),(61,{self.usrid}),(62,{self.usrid}),(63,{self.usrid}),(64,{self.usrid});"
            )
            cur[1].commit()
            self.add_course("LUNCH", 5 * 4 * 6)
            self.add_course("FREE", 0)
            self.add_course("MEET", 6 * 4)
        except Exception as error:
            print ("Oops! An exception has occured:", error)
            print ("Exception TYPE:", type(error))
            print("Could not create User Data")

    def check_id(self, cur=None):
        if cur is None:
            cur = self.create_cur(self.connect_db())
        try:
            cur[0].execute(
                f"SELECT usrid FROM authentication WHERE usrid={self.usrid}"
            )
            return cur[0].fetchone() is None
        except Exception as error:
            print ("Oops! An exception has occured:", error)
            print ("Exception TYPE:", type(error))
            return False

    def check_password(self, cur=None):
        if cur is None:
            cur = self.create_cur(self.connect_db())
        try:
            cur[0].execute(
                f"SELECT password FROM authentication WHERE usrid={self.usrid}"
            )
            return cur[0].fetchone() == self.password

        except Exception as error:
            print ("Oops! An exception has occured:", error)
            print ("Exception TYPE:", type(error))
            return False

    def reset_db(self, cur=None):
        if cur is None:
            cur = self.create_cur(self.connect_db())
        try:
            cur[0].execute("DROP TABLE IF EXISTS jobs CASCADE")
            cur[0].execute("DROP TABLE IF EXISTS courses CASCADE")
            cur[0].execute("DROP TABLE IF EXISTS courses_cpy CASCADE")
            cur[0].execute("DROP TABLE IF EXISTS authentication CASCADE")
            cur[0].execute(
                "CREATE TABLE authentication (usrid NUMERIC(12) NOT NULL PRIMARY KEY, password NUMERIC(12) NOT NULL)"
            )
            cur[0].execute(
                "CREATE TABLE courses (code VARCHAR(8) NOT NULL PRIMARY KEY, hours INTEGER NOT NULL,usrid NUMERIC(12) NOT NULL REFERENCES authentication(usrid))"
            )
            cur[0].execute(
                "CREATE TABLE courses_cpy (code VARCHAR(8) NOT NULL PRIMARY KEY REFERENCES courses(code), hours INTEGER NOT NULL, usrid NUMERIC(12) NOT NULL REFERENCES authentication(usrid))"
            )
            cur[0].execute(
                "CREATE TABLE jobs (hour NUMERIC(2) NOT NULL PRIMARY KEY, code VARCHAR(8) REFERENCES courses(code),usrid NUMERIC(12) NOT NULL REFERENCES authentication(usrid))"
            )
            cur[0].execute(
                """CREATE OR REPLACE FUNCTION byfor()
            RETURNS trigger as $byfor$
            declare
            hrs integer;
            BEGIN
            hrs=CEIL(new.hours/24);
            INSERT INTO courses_cpy VALUES (new.code, hrs, new.usrid);
            RETURN NEW;
            END;
            $byfor$
            LANGUAGE plpgsql;
            CREATE OR REPLACE TRIGGER byfor AFTER INSERT ON courses FOR EACH ROW EXECUTE PROCEDURE byfor();"""
            )
            cur[0].execute(
                """CREATE OR REPLACE FUNCTION decl()
            RETURNS trigger as $decl$
            declare
            hrs integer;
            BEGIN
            SELECT hours into hrs FROM courses_cpy WHERE code=new.code;
            hrs=hrs-1;
            UPDATE courses_cpy
            SET hours = hrs
            WHERE code = new.code;
            RETURN NEW;
            END;
            $decl$
            LANGUAGE plpgsql;
            CREATE OR REPLACE TRIGGER decl AFTER UPDATE ON jobs FOR EACH ROW EXECUTE PROCEDURE decl();"""
            )

            cur[1].commit()

            return True
        except Exception as error:
            print ("Oops! An exception has occured:", error)
            print ("Exception TYPE:", type(error))
            print("The DataBase Couldnt be Reset")
            return False
