import os
import mysql.connector

def getConnection():
    try:
        conn = mysql.connector.connect(host = os.environ.get("DB_HOST", "127.0.0.1"),
                                       user = os.environ["DB_USER"],
                                       password = os.environ["DB_PASSWORD"],
                                       database = os.environ["DB_NAME"]
        )
        return conn
    except mysql.connector.Error as error:
        print(f"Database connection failed: {error}")
        return None

