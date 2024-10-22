# plugins/postgres_plugin.py
from plugins.plugin_base import Plugin

class PostgresPlugin(Plugin):
    def __init__(self, config):
        super().__init__()
        self.config = config  # Store the passed configuration
        self.client = None  # Initialize client as None
        
    def setup(self):
        print("Setting up PostgreSQL connection")

    def run(self):
        print("Running PostgreSQL benchmarks")

    def teardown(self):
        print("Tearing down PostgreSQL connection")
