import psycopg2
import json
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler

class Database:
    def __init__(self, host, port, user, password, database):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database

    def connect(self):
        try:
            conn = psycopg2.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database
            )
            return conn
        except psycopg2.Error as e:
            print("Error connecting to database:", e)
            return None

    def close(self, conn, cur=None):
        try:
            if cur is not None:
                cur.close()
            if conn is not None:
                conn.close()
        except psycopg2.Error as e:
            print("Error closing database connection:", e)