# plugins/db_test_plugin.py
from modules.db_connect import connect_to_database, close_database_connection
from modules.sysbench_test import prepare_database, perform_sysbench_test, parse_sysbench_output
from modules.sysbench_install import ssh_connect, install_sysbench, ssh_connect_azure_vm
from modules.file_transfer import transfer_file_from_vm
from modules.plot_dashboard import plot_sysbench_dashboard
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
        
        print("Preparing database for running Sysbench test...")
        #self.client = ssh_connect(self.config)
        self.client = ssh_connect_azure_vm(self.config)
        
        # Check Sysbench installed or not
        #install_sysbench(self.client, self.config)

        # Prepare Database
        print("Running Sysbench for preparaing database...")
        #prepare_database(self.client, self.config)
        
        print("Running Sysbench test for Database performance...")
        # Perform test for performance
        perform_sysbench_test(self.client, self.config)
        
        # Transfer output file
        print("Transferring sysbench metrics file...")
        transfer_file_from_vm(self.client, 'pgsql10_thread20.txt', './outputs/aws/Database/postgresql/thread20/test10.txt')
        print("Parsing sysbench output...")
        df_intermediate, final_stats, latency_stats, fairness_stats = parse_sysbench_output('./outputs/aws/Database/postgresql/thread20/test10.txt')
        
        if not df_intermediate.empty:
            print("Saving parsed data to CSV...")
            df_intermediate.to_csv("./outputs/sysbench_intermediate.csv", index=False)
            Series(final_stats).to_csv('./outputs/sysbench_sql_stats.csv')
            Series(latency_stats).to_csv('./outputs/sysbench_latency_stats.csv')
            Series(fairness_stats).to_csv('./outputs/sysbench_fairness_stats.csv')
        else:
            print("Parsed data is empty. Check the input file or parsing logic.")

       # plot_sysbench_dashboard()
        

    def teardown(self):
        print("Closing the database connection...")
        #if self.connection:
         #   close_database_connection(self.connection)
