# plugins/sysbench_plugin.py
from sysbench_install import install_sysbench, ssh_connect
from plugins.plugin_manager import Plugin

class SysbenchPlugin(Plugin):
    def __init__(self, config):
        super().__init__()
        self.config = config  # Store the passed configuration
        self.client = None  # Initialize client as None

    def setup(self):
        print("Setting up SSH and Sysbench installation...")
        

    def run(self):
        print("Establishing SSH connection and installing Sysbench...")
        self.client = ssh_connect(self.config)
        if self.client:
            install_sysbench(self.client)
        else:
            print("Failed to establish SSH connection.")
            return False  # Return False to stop the pipeline if critical step fails

    def teardown(self):
        print("Closing the SSH connection...")
        if self.client:
            self.client.close()
