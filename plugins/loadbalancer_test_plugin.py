# plugins/loadbalancer_test_plugin.py
from modules.sysbench_test import ssh_connect
from modules.loadbalancer_test import perform_ab_test, install_ab, parse_ab_output
from modules.file_transfer import transfer_file_from_vm
from plugins.plugin_manager import Plugin
from pandas import DataFrame

class LoadbalancerTestPlugin(Plugin):
    def __init__(self, config):
        super().__init__()
        self.config = config  # Store the passed configuration
        self.client = None  # Initialize client as None

    def setup(self):
        print("Setting up for Load Balancer test...")
        

    def run(self):
        print("Preparing, Installation and running Apache benchmark test...")
        self.client = ssh_connect(self.config)
        #Check ab is installed or not If not installed earlied then install it.
        install_ab(self.client, self.config)

        #prepare_database(self.client, self.config)
        perform_ab_test(self.client, self.config)
        
        print("Transferring Apache benchmark metrics file...")
        transfer_file_from_vm(self.client, 'ab_metrics.txt', './outputs/ab_metrics.txt')

        print("Parsing ab output...")

        # Parse the ab_metrics.txt file
        summary_stats, connection_times_df, percentiles_df = parse_ab_output('./outputs/ab_metrics.txt')

        if summary_stats:
            print("Summary_state data to CSV...")

            # Save summary statistics to a CSV file
            DataFrame([summary_stats]).to_csv("./outputs/ab_summary_stats.csv", index=False)
        else:
            print("Summary_state data is empty. Check the input file or parsing logic.")

            # Save connection times and latency percentiles
        if not connection_times_df.empty:
            print("Connection time is saving ...")
            connection_times_df.to_csv('./outputs/ab_connection_times.csv', index=False)
        else:
            print("Connection_time data is empty. Check the input file or parsing logic.")
        if not percentiles_df.empty:
            print("Percentiles is saving...")
            percentiles_df.to_csv('./outputs/ab_percentiles.csv', index=False)
            

        else:
            print("Percentile data is empty. Check the input file or parsing logic.")


    def teardown(self):
        print("Tearing down test...")
        if self.client:
            self.client.close()
