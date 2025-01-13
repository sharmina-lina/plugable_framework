# plugins/sysbench_test_plugin.py
from sysbench_install import ssh_connect
from loadbalancer_test import perform_ab_test, install_ab
from file_transfer import transfer_file_from_vm
from plugins.plugin_manager import Plugin

class LoadBalancerPlugin(Plugin):
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

    def teardown(self):
        print("Tearing down test...")
        if self.client:
            self.client.close()
