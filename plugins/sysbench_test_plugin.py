# plugins/sysbench_test_plugin.py
from sysbench_test import perform_sysbench_test, prepare_database, ssh_connect
from file_transfer import transfer_file_from_vm
from plugins.plugin_manager import Plugin

class SysbenchTestPlugin(Plugin):
    def __init__(self, config):
        super().__init__()
        self.config = config  # Store the passed configuration
        self.client = None  # Initialize client as None

    def setup(self):
        print("Setting up Sysbench test...")
        

    def run(self):
        # Estblish connection
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

    def teardown(self):
        print("Tearing down Sysbench test...")
        if self.client:
            self.client.close()
