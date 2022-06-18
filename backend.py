import psycopg2
import sys
from psycopg2 import connect
from psycopg2 import OperationalError, errorcodes, errors


class DataBase:
    def __init__(self, usrid, password):
        """
        The function __init__() is a constructor that initializes the attributes of the class

        :param usrid: The username of the account you want to log into
        :param password: The password for the user
        """
        self.ids = usrid
        self.pswd = password

    def connect_db(self):
        """
        It connects to the database and returns a connection object
        :return: A connection object.
        """
        return psycopg2.connect(
            user="postgres",
            password="1024",
            host="localhost",
            port="5432",
            database="ttdb",
        )

    def create_cur(self, conn):
        """
        It creates a cursor and returns it along with the connection

        :param conn: The connection object
        :return: A tuple of the cursor and the connection.
        """
        return (conn.cursor(), conn)

    def check_id(self, cur=None):
        """
        It checks if the user id exists in the database

        :param cur: The cursor object
        :return: a boolean value.
        """
        if cur is None:
            cur = self.create_cur(self.connect_db())
        try:
            cur[0].execute(
                f"SELECT usrid FROM authentication WHERE usrid = {self.ids}"
            )
            return cur[0].fetchone() is not None
        except Exception as error:
            print ("Oops! An exception has occurred:", error)
            print ("Exception TYPE:", type(error))
            return False

    def check_password(self, cur=None):
        """
        It takes a user's id and password, and checks if the password is correct

        :param cur: a cursor object
        :return: The password from the database is being returned.
        """
        if cur is None:
            cur = self.create_cur(self.connect_db())
        try:
            cur[0].execute(
                f"SELECT password FROM authentication WHERE usrid={self.ids}"
            )
            return cur[0].fetchone()[0] == self.pswd

        except Exception as error:
            print ("Oops! An exception has occurred:", error)
            print ("Exception TYPE:", type(error))
            return False

    def set_password(self,cur=None):
        """
        It updates the password of a user in the database

        :param cur: This is the cursor object that is returned by the create_cur() method
        :return: A boolean value
        """
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
            print("Password not updated")
            return False


    def create_user(self, cur=None):
        """
        It deletes the user's data from the database and then inserts the new data

        :param cur: This is the cursor object that is returned by the create_cur() function
        """
        if cur is None:
            cur = self.create_cur(self.connect_db())
        try:
            cur[0].execute(f"DELETE FROM authentication WHERE usrid={self.ids};")
            cur[0].execute(
                f"INSERT INTO authentication VALUES ({self.ids},{self.pswd});")
            cur[1].commit()
        except Exception as error:
            print ("Oops! An exception has occurred:", error)
            print ("Exception TYPE:", type(error))
            print("Could not create User Data")

    def delete_user(self, cur=None):
        """
        It deletes a user from the database

        :param cur: The cursor object
        :return: a boolean value.
        """
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

    def add_course(self, code, hours, cur=None):
        """
        It adds a course to the database

        :param code: The course code
        :param hours: int
        :param cur: a cursor object
        :return: A list of tuples.
        """
        if cur is None:
            cur = self.create_cur(self.connect_db())
        try:
            cur[0].execute(f"INSERT INTO courses VALUES ( '{code}', {hours} )")
            cur[1].commit()
            return True
        except Exception as error:
            print ("Oops! An exception has occurred:", error)
            print ("Exception TYPE:", type(error))
            return False

    def get_course(self, cur=None, code=None, hours=0 ):
        """
        This function returns a list of tuples containing the course code, course name, and number of
        hours for all courses in the database that have a number of hours greater than or equal to the
        number of hours specified by the user

        :param cur: the cursor object
        :param code: the course code
        :param hours: the minimum number of hours for the course, defaults to 0 (optional)
        :return: A list of tuples.
        """
        if cur is None:
            cur = self.create_cur(self.connect_db())
        try:
            if code is None:
                cur[0].execute(f"SELECT * FROM courses WHERE hours >= {hours} ORDER BY code;")
            else:
                cur[0].execute(f"SELECT * FROM courses WHERE code = '{code}' AND hours >= {hours} ORDER BY code;")
            return cur[0].fetchall()
        except Exception as error:
            print ("Oops! An exception has occured:", error)
            print ("Exception TYPE:", type(error))
            print("course code not found")
            return None

    def delete_course(self, code=None, hours=0, cur=None):
        """
        It deletes a course from the database

        :param code: the course code
        :param hours: the number of hours the course takes, defaults to 0 (optional)
        :param cur: a cursor object
        :return: A boolean value.
        """
        if cur is None:
            cur = self.create_cur(self.connect_db())

        if code is None:
            return False
        try:
            cur[0].execute(f"UPDATE slots SET code = NULL WHERE code = '{code}';")
            cur[0].execute(f"DELETE FROM classes WHERE code='{code}';")
            cur[0].execute(f"DELETE FROM constraints WHERE code='{code}';")
            cur[0].execute(f"DELETE FROM courses WHERE code='{code}'AND hours={hours};")
            cur[1].commit()
            return True
        except Exception as error:
            print ("Oops! An exception has occurred:", error)
            print ("Exception TYPE:", type(error))
            print("course not deleted")
            return False

    def add_clss(self, clss, code, cur=None):
        """
        It takes a class name and a class code and adds it to the database

        :param clss: The name of the class
        :param code: The code of the class
        :param cur: The cursor object
        :return: A boolean value.
        """
        if cur is None:
            cur = self.create_cur(self.connect_db())
        try:
            cur[0].execute(f"INSERT INTO classes VALUES ( '{clss}', '{code}' )")
            cur[1].commit()
            return True
        except Exception as error:
            print ("Oops! An exception has occurred:", error)
            print ("Exception TYPE:", type(error))
            return False

    def get_clss(self, clss=None, cur=None, code=None):
        """
        This function returns a list of tuples containing the class and code of the class that is passed
        in as a parameter

        :param cur: The cursor object. If not provided, a new cursor object will be created
        :param clss: The class you want to get the data from
        :param code: The code of the class
        :return: the class and code of the class.
        """
        if cur is None:
            cur = self.create_cur(self.connect_db())
        try:
            if clss is None:
                cur[0].execute(f"SELECT * FROM classes ORDER BY class;")
            elif code is None:
                cur[0].execute(f"SELECT * FROM classes WHERE class='{clss}' ORDER BY class;")
            else:
                cur[0].execute(f"SELECT * FROM classes WHERE class = '{clss}' AND code = '{code}' ORDER BY class;")
            return cur[0].fetchall()
        except Exception as error:
            print ("Oops! An exception has occurred:", error)
            print ("Exception TYPE:", type(error))
            print("Class not found")
            return None

    def delete_clss(self, clss=None, code=None, cur=None):
        """
        It deletes a class from the database

        :param clss: The class name
        :param code: The code of the class, defaults to 0 (optional)
        :param cur: the cursor object
        :return: A boolean value.
        """
        if cur is None:
            cur = self.create_cur(self.connect_db())
        try:
            if code is None:
                cur[0].execute(f"DELETE FROM slots WHERE class = '{clss}';")
                cur[0].execute(f"DELETE FROM constraints WHERE class='{clss}';")
                cur[0].execute(f"DELETE FROM classes WHERE class='{clss}';")
            else:
                cur[0].execute(f"UPDATE slots SET code = NULL WHERE class = '{clss}' AND code='{code}';")
                cur[0].execute(f"DELETE FROM classes WHERE class='{clss}' AND code='{code}';")
                cur[0].execute(f"DELETE FROM constraints WHERE class='{clss}' AND code='{code}';")
                cur[1].commit()
            return True
        except Exception as error:
            print ("Oops! An exception has occurred:", error)
            print ("Exception TYPE:", type(error))
            print("class not deleted")
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

    def reset_dib(self, cur=None):
        # A function that resets the database.
        if cur is None:
            cur = self.create_cur(self.connect_db())
        try:
            cur[0].execute("DROP TABLE IF EXISTS slots CASCADE")
            cur[0].execute("DROP TABLE IF EXISTS courses CASCADE")
            cur[0].execute("DROP TABLE IF EXISTS classes CASCADE")
            cur[0].execute("DROP TABLE IF EXISTS authentication CASCADE")
            cur[0].execute("DROP TABLE IF EXISTS constraints CASCADE")
            cur[0].execute(
                "CREATE TABLE authentication (usrid NUMERIC(12) NOT NULL PRIMARY KEY, password NUMERIC(12) NOT NULL)"
            )
            cur[0].execute(
                "CREATE TABLE courses (code VARCHAR(8) NOT NULL PRIMARY KEY, hours INTEGER NOT NULL)"
            )
            cur[0].execute(
                "CREATE TABLE classes (class VARCHAR(8) NOT NULL, code VARCHAR(8) REFERENCES courses(code), PRIMARY KEY(class,code))"
            )
            cur[0].execute(
                "CREATE TABLE slots (slot_no NUMERIC(2) NOT NULL, code VARCHAR(8) REFERENCES courses(code), class VARCHAR(8)  , PRIMARY KEY(class,slot_no))"
            )
            cur[0].execute(
                "CREATE TABLE constraints (code VARCHAR(8) REFERENCES courses(code) NOT NULL, slot_no NUMERIC(2) NOT NULL, class VARCHAR(8)   NOT NULL, PRIMARY KEY (code, slot_no, class))"
            )
            cur[1].commit()
            return True
        except Exception as error:
            print ("An exception has occured:", error)
            print ("Exception TYPE:", type(error))
            print("The DataBase Couldnt be Reset")
            return False

def reset_db():
    DataBase(0,0).reset_dib()

print(DataBase(0,0).get_course())