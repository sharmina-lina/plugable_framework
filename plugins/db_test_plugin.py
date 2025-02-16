# plugins/db_test_plugin.py
from functions.db_connect import connect_to_database, close_database_connection
from functions.sysbench_test import prepare_database, perform_sysbench_test, parse_sysbench_output, ssh_connect
from functions.file_transfer import transfer_file_from_vm
from plugins.plugin_manager import Plugin
from pandas import Series

class DbTestPlugin(Plugin):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.db_config = self.config['database']
        self.connection = None
        self.client = None

    def setup(self):
        print("Setting up database connection for sysbench test...")

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
        
        print("Preparing database for running Sysbench test...")
        self.client = ssh_connect(self.config)
        # Prepare Database
        prepare_database(self.client, self.config)
        
        print("Running Sysbench test for Database performance...")
        # Perform test for performance
        perform_sysbench_test(self.client, self.config)
        
        # Transfer output file
        print("Transferring sysbench metrics file...")
        transfer_file_from_vm(self.client, 'sysbench_metrics.txt', './outputs/sysbench_metrics.txt')

        print("Parsing sysbench output...")
        df_intermediate, final_stats, latency_stats, fairness_stats = parse_sysbench_output('./outputs/sysbench_metrics.txt')
        
        if not df_intermediate.empty:
            print("Saving parsed data to CSV...")
            df_intermediate.to_csv("./outputs/sysbench_intermediate.csv", index=False)
            Series(final_stats).to_csv('./outputs/sysbench_sql_stats.csv')
            Series(latency_stats).to_csv('./outputs/sysbench_latency_stats.csv')
            Series(fairness_stats).to_csv('./outputs/sysbench_fairness_stats.csv')
        else:
            print("Parsed data is empty. Check the input file or parsing logic.")

        
        

    def teardown(self):
        print("Closing the database connection...")
        if self.connection:
            close_database_connection(self.connection)
