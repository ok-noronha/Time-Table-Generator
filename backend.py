import psycopg2
import sys
from psycopg2 import connect
from psycopg2 import OperationalError, errorcodes, errors


class DataBase:
    def __init__(self, usrid, password):
        self.ids = usrid
        self.pswd = password

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
            cur[0].execute(f"INSERT INTO courses VALUES ( '{code}',{hours},{self.ids})")
            cur[1].commit()
            return True
        except Exception as error:
            print ("Oops! An exception has occured:", error)
            print ("Exception TYPE:", type(error))
            return False

    def get_courses(self, cur=None):
        if cur is None:
            cur = self.create_cur(self.connect_db())
        try:
            cur[0].execute(f"SELECT * FROM courses WHERE usrid={self.ids};")
            return cur[0].fetchall()
        except Exception as error:
            print ("Oops! An exception has occured:", error)
            print ("Exception TYPE:", type(error))
            print("course code not found")
            return None

    def set_password(self,cur=None):
        if cur is None:
            cur = self.create_cur(self.connect_db())
        try:
            cur[0].execute(f"UPDATE authentication SET password={self.pswd} WHERE usrid={self.ids}")
            cur[1].commit()
            print("Password updated")
            return True
        except Exception as error:
            print ("Oops! An exception has occured:", error)
            print ("Exception TYPE:", type(error))
            print("course not deleted")
            print("Password not updated")
            return False


    def delete_course(self, code, cur=None):
        if cur is None:
            cur = self.create_cur(self.connect_db())
        try:
            cur[0].execute(f"DELETE FROM courses_cpy WHERE code='{code}'AND usrid={self.ids};")
            cur[0].execute(f"DELETE FROM courses WHERE code='{code}'AND usrid={self.ids};")
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
            cur[0].execute(f"SELECT hour FROM jobs WHERE code IS NULL AND usrid={self.ids};")
            jobs=cur[0].fetchall()
            for job in jobs:
                cod=None
                if (job[0]%10 == 1):
                    try:
                        cur[0].execute(f"SELECT code, hours FROM courses_cpy WHERE usrid={self.ids} AND code NOT IN ('LUNCH','MEET','FREE') AND hours>0 ORDER BY random() LIMIT 1")
                        cod = cur[0].fetchone()[0]
                        if cod is None:
                            raise Exception("No Mandatory Courses")
                    except Exception as e:
                        cur[0].execute(f"SELECT code, hours  FROM courses_cpy WHERE usrid={self.ids} AND code NOT IN ('LUNCH','MEET','FREE') ORDER BY random() LIMIT 1")
                        cod = cur[0].fetchone()[0]
                else :
                    try:
                        cur[0].execute(f"SELECT code, hours  FROM courses_cpy WHERE usrid={self.ids} AND code NOT IN ('LUNCH') AND hours>0 ORDER BY random() LIMIT 1")
                        cod = cur[0].fetchone()[0]
                        if cod is None:
                            raise Exception("No Mandatory Courses")
                    except Exception as e:
                        cur[0].execute(f"SELECT code, hours FROM courses_cpy WHERE usrid={self.ids} AND code NOT IN ('LUNCH') ORDER BY random() LIMIT 1")
                        cod = cur[0].fetchone()[0]
                cur[0].execute(
                    f"""UPDATE jobs
                SET code = '{cod}'
                WHERE hour={job[0]}"""
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
            cur[0].execute(f"SELECT * FROM jobs WHERE usrid={self.ids};")
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
            cur[0].execute(f"DELETE FROM jobs WHERE usrid={self.ids};")
            cur[0].execute(f"DELETE FROM courses_cpy WHERE usrid={self.ids};")
            cur[0].execute(f"DELETE FROM courses WHERE usrid={self.ids};")
            cur[0].execute(f"DELETE FROM authentication WHERE usrid={self.ids};")
            cur[0].execute(
                f"INSERT INTO authentication VALUES ({self.ids},{self.pswd});")
            cur[0].execute(
                f"INSERT INTO jobs (hour,usrid) VALUES (11,{self.ids}),(12,{self.ids}),(13,{self.ids}),(14,{self.ids}),(15,{self.ids}),(16,{self.ids}),(17,{self.ids}),(21,{self.ids}),(22,{self.ids}),(23,{self.ids}),(24,{self.ids}),(25,{self.ids}),(26,{self.ids}),(27,{self.ids}),(31,{self.ids}),(32,{self.ids}),(33,{self.ids}),(34,{self.ids}),(35,{self.ids}),(36,{self.ids}),(37,{self.ids}),(41,{self.ids}),(42,{self.ids}),(43,{self.ids}),(44,{self.ids}),(45,{self.ids}),(46,{self.ids}),(47,{self.ids}),(51,{self.ids}),(52,{self.ids}),(53,{self.ids}),(54,{self.ids}),(55,{self.ids}),(56,{self.ids}),(57,{self.ids}),(61,{self.ids}),(62,{self.ids}),(63,{self.ids}),(64,{self.ids});"
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
                f"SELECT usrid FROM authentication WHERE usrid = {self.ids}"
            )
            return cur[0].fetchone() is not None
        except Exception as error:
            print ("Oops! An exception has occured:", error)
            print ("Exception TYPE:", type(error))
            return False

    def delete_user(self, cur=None):
        if cur is None:
            cur = self.create_cur(self.connect_db())
        try:
            cur[0].execute(
                f"DELETE FROM authentication WHERE usrid={self.ids}"
            )
            return True
        except Exception as error:
            print ("Oops! An exception has occured:", error)
            print ("Exception TYPE:", type(error))
            return False

    def check_password(self, cur=None):
        if cur is None:
            cur = self.create_cur(self.connect_db())
        try:
            cur[0].execute(
                f"SELECT password FROM authentication WHERE usrid={self.ids}"
            )
            return cur[0].fetchone()[0] == self.pswd

        except Exception as error:
            print ("Oops! An exception has occured:", error)
            print ("Exception TYPE:", type(error))
            return False

    def reset_dib(self, cur=None):
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
                "CREATE TABLE courses (code VARCHAR(8) NOT NULL , hours INTEGER NOT NULL,usrid NUMERIC(12) NOT NULL REFERENCES authentication(usrid) ON DELETE CASCADE)"
            )
            cur[0].execute(
                "CREATE TABLE courses_cpy (code VARCHAR(8) NOT NULL , hours INTEGER NOT NULL, usrid NUMERIC(12) NOT NULL REFERENCES authentication(usrid) ON DELETE CASCADE)"
            )
            cur[0].execute(
                "CREATE TABLE jobs (hour NUMERIC(2) NOT NULL , code VARCHAR(8) ,usrid NUMERIC(12) NOT NULL REFERENCES authentication(usrid) ON DELETE CASCADE)"
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
                f"""CREATE OR REPLACE FUNCTION decl()
            RETURNS trigger as $decl$
            declare
            hrs integer;
            BEGIN
            SELECT hours into hrs FROM courses_cpy WHERE code=new.code;
            hrs=hrs-1;
            UPDATE courses_cpy
            SET hours = hrs
            WHERE code = new.code AND usrid = {self.ids};
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

def reset_db():
    DataBase(0,0).reset_dib()
