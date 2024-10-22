# plugins/mysql_plugin.py
from plugins.plugin_base import Plugin

class MysqlPlugin(Plugin):
    def __init__(self, config):
        super().__init__()
        self.config = config  # Store the passed configuration
        self.client = None  # Initialize client as None
        
    def setup(self):
        print("Setting up MySQL connection")

    def run(self):
        print("Running MySQL benchmarks")

    def teardown(self):
        print("Tearing down MySQL connection")
