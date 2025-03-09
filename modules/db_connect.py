## modules/db_connect.py
import mysql.connector
#import sqlite3
from mysql.connector import Error as MySQLError
#from sqlite3 import Error as SQLiteError
#from pymongo import MongoClient
#import cx_Oracle
#import psycopg2

# MySQL Connection Function
def connect_to_mysql(db_config):
    try:
        connection = mysql.connector.connect(
            host=db_config['host'],
            port=db_config['port'],
            database=db_config['db_name'],
            user=db_config['username'],
            password=db_config['password']
        )
        if connection.is_connected():
            print("Successfully connected to the MySQL database")
            return connection
    except MySQLError as e:
        print(f"MySQL Error: {e}")
        return None

# PostgreSQL Connection Function
def connect_to_postgresql(db_config):
    try:
        connection = psycopg2.connect(
            host=db_config['host'],
            port=db_config['port'],
            database=db_config['db_name'],
            user=db_config['username'],
            password=db_config['password']
        )
        print("Successfully connected to the PostgreSQL database")
        return connection
    except PostgreSQLError as e:
        print(f"PostgreSQL Error: {e}")
        return None

# SQLite Connection Function
def connect_to_sqlite(db_config):
    try:
        connection = sqlite3.connect(db_config['db_name'])
        print("Successfully connected to the SQLite database")
        return connection
    except SQLiteError as e:
        print(f"SQLite Error: {e}")
        return None

# MongoDB Connection Function
def connect_to_mongodb(db_config):
    try:
        # MongoClient to connect to MongoDB instance
        client = MongoClient(
            host=db_config['host'],
            port=int(db_config['port']),
            username=db_config['username'],
            password=db_config['password']
        )
        db = client[db_config['db_name']]
        print("Successfully connected to the MongoDB database")
        return db
    except Exception as e:
        print(f"MongoDB Error: {e}")
        return None

# Redis Connection Function
def connect_to_redis(db_config):
    try:
        connection = redis.StrictRedis(
            host=db_config['host'],
            port=db_config['port'],
            password=db_config.get('password'),  # Password is optional
            decode_responses=True
        )
        # Test the connection
        if connection.ping():
            print("Successfully connected to the Redis database")
            return connection
    except Exception as e:
        print(f"Redis Error: {e}")
        return None

# MariaDB Connection Function
def connect_to_mariadb(db_config):
    try:
        connection = mysql.connector.connect(
            host=db_config['host'],
            port=db_config['port'],
            database=db_config['db_name'],
            user=db_config['username'],
            password=db_config['password'],
            
        )
        if connection.is_connected():
            print("Successfully connected to the MariaDB database with adjusted collation")
            return connection
            
    except MySQLError as e:
        print(f"MariaDB Error: {e}")
        return None

# InfluxDB Connection Function
def connect_to_influxdb(db_config):
    try:
        client = InfluxDBClient(
            host=db_config['host'],
            port=db_config['port'],
            username=db_config['username'],
            password=db_config['password'],
            database=db_config['db_name']
        )
        # Check if the database exists
        if db_config['db_name'] in [db['name'] for db in client.get_list_database()]:
            print("Successfully connected to the InfluxDB database")
            return client
    except Exception as e:
        print(f"InfluxDB Error: {e}")
        return None


# Oracle Connection Function
def connect_to_oracle(db_config):
    try:
        dsn = cx_Oracle.makedsn(db_config['host'], db_config['port'], sid=db_config['db_name'])
        connection = cx_Oracle.connect(
            user=db_config['username'],
            password=db_config['password'],
            dsn=dsn
        )
        print("Successfully connected to the Oracle database")
        return connection
    except cx_Oracle.DatabaseError as e:
        print(f"Oracle Error: {e}")
        return None

# Dispatcher to select the appropriate connection function
def connect_to_database(db_config):
    db_type = db_config.get('db_type')
    
    if db_type == "mysql":
        print("Connecting to MySQL...")
        return connect_to_mysql(db_config)
    #elif db_type == "postgresql":
     #   return connect_to_postgresql(db_config)
    elif db_type == "sqlite":
        return connect_to_sqlite(db_config)
    elif db_type == "mongodb":
        return connect_to_mongodb(db_config)
    elif db_type == "oracle":
        return connect_to_oracle(db_config)
    elif db_type == "redis":
        return connect_to_redis(db_config)
    elif db_type == "mariadb":
        return connect_to_mariadb(db_config)
    elif db_type == "influxdb":
        return connect_to_influxdb(db_config)
    else:
        print(f"Unsupported database type: {db_type}")
        return None

# Function to close the connection
def close_database_connection(connection):
    if connection:
        connection.close()
        print("Database connection closed.")
