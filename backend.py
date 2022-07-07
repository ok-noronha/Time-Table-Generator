import psycopg2
import sys
from psycopg2 import connect
from psycopg2 import OperationalError, errorcodes, errors

slotss=[11,12,13,14,15,16,17,21,22,23,24,25,26,27,31,32,33,34,35,36,37,41,42,43,44,45,46,47,51,52,53,54]
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

    def add_constraint(self, clss=None, code=None, slot=None, cur=None):
        """
        It takes in a class, a code, a slot, and a cursor, and inserts the class, code, and slot into
        the constraints table

        :param clss: The class code
        :param code: the code of the constraint
        :param slot: the slot number
        :param cur: a cursor object
        :return: A boolean value.
        """
        if cur is None:
            cur = self.create_cur(self.connect_db())
        try:
            cur[0].execute(f"INSERT INTO constraints VALUES ( '{code}', {slot}, '{clss}' )")
            cur[1].commit()
            return True
        except Exception as error:
            print ("Oops! An exception has occurred:", error)
            print ("Exception TYPE:", type(error))
            return False

    def get_constraint(self, cur=None, code=None, clss=None, slot=None):
        """
        This function returns all the constraints in the database

        :param cur: the cursor object
        :param code: the code of the class
        :param clss: The class name
        :param slot: the slot name
        :return: A list of tuples.
        """
        if cur is None:
            cur = self.create_cur(self.connect_db())
        try:
            if clss is None and code is None and slot is None:
                cur[0].execute(f"SELECT * FROM constraints ORDER BY class;")
            elif code is None and slot is None:
                cur[0].execute(f"SELECT * FROM constraints WHERE class = '{clss}';")
            else:
                pass
                #cur[0].execute(f"SELECT * FROM classes WHERE class = '{clss}' AND code = '{code}' ORDER BY class;")
            return cur[0].fetchall()
        except Exception as error:
            print ("Oops! An exception has occurred:", error)
            print ("Exception TYPE:", type(error))
            print("Class not found")
            return None

    def delete_constraint(self, cur=None, code=None, clss=None, slot=None):
        """
        It deletes a constraint from the database

        :param code: The code of the course
        :param clss: The class for which the constraint is being added
        :param slot: The slot number of the constraint
        :return: a boolean value.
        """
        if cur is None:
            cur = self.create_cur(self.connect_db())

        if code is None:
            return False
        try:
            cur[0].execute(f"DELETE FROM constraints WHERE code='{code}'AND class='{clss}' AND slot_no={slot};")
            cur[1].commit()
            return True
        except Exception as error:
            print ("Oops! An exception has occurred:", error)
            print ("Exception TYPE:", type(error))
            print("course not deleted")
            return False

    def reset_dib(self, cur=None):
        """
        It resets the database

        :param cur: A cursor object
        :return: a boolean value.
        """
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
            print ("An exception has occurred:", error)
            print ("Exception TYPE:", type(error))
            print("The DataBase couldn't be Reset")
            return False

def reset_db():
    DataBase(0,0).reset_dib()
