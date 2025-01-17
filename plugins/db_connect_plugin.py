# plugins/db_connect_plugin.py
from db_connect import connect_to_database, close_database_connection
from plugins.plugin_manager import Plugin

class DbConnectPlugin(Plugin):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.db_config = self.config['database']
        self.connection = None

    def setup(self):
        print("Setting up database connection...")

    def run(self):
        if self.connection:
            print("Already connected to the database. Skipping reconnection.")
            return True  # Connection is already established
        print("Connecting to the database...")
        self.connection = connect_to_database(self.db_config)
        if self.connection:
            print("Database connection successful.")
        else:
            print("Failed to connect to the database. Exiting.")
            return False  # Stop the pipeline if critical step fails

    def teardown(self):
        print("Closing the database connection...")
        if self.connection:
            close_database_connection(self.connection)
