# Program for establish connection from anywhere to Database that are located in any cloud
import mysql.connector
from mysql.connector import Error
import yaml

    
# Function to establishing the connection with database from the local machine

def connect_to_database(db_config):
    try:
        connection = mysql.connector.connect(
         
            host=db_config['host'],
            port=db_config['port'],  # Convert port to string
            database=db_config['db_name'],
            user=db_config['username'],
            password=db_config['password']
        )
        if connection.is_connected():
            print("Successfully connected to the database")
            return connection
        else:
            print("Failed to connect to the database")
            return None
    except Error as e:
        print(f"Error: {e}")
        return None

def close_database_connection(connection):
    # Ensure proper connection closure
    if connection.is_connected():
        connection.close()
        print("Database connection closed.")
