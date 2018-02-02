import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return None


def execute_query(db_file, sql, values=None):
    try:
        # Creates or opens a file called mydb with a SQLite3 DB
        db = create_connection(db_file)
        # Get a cursor object
        cursor = db.cursor()
        # Check if table users does not exist and create it
        if values is None:
            cursor.execute(sql)
        else:
            cursor.execute(sql, values)
        # Commit the change
        db.commit()

        results = []
        for row in cursor:
            results.append(row)
    # Catch the exception
    except Exception as e:
        # Roll back any change if something goes wrong
        db.rollback()
        print(e)
        raise e
    finally:
        # Close the db connection
        db.close()
        return results

