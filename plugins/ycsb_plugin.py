import subprocess
from plugins.plugin_manager import Plugin

class YcsbPlugin(Plugin):
    def __init__(self, config):
        super().__init__()
        self.config = config

    def setup(self):
        print("Setting up YCSB test...")

    def run(self):
        print("Running YCSB benchmark...")
        db_type = self.config['database']['db_type']
        host = self.config['database']['host']
        port = self.config['database']['port']
        db_name = self.config['database']['db_name']

        ycsb_command = (
            f"./bin/ycsb run {db_type} "
            f"-P workloads/workloada "
            f"-p {db_type}.url=jdbc:{db_type}://{host}:{port}/{db_name} "
            f"-p {db_type}.user={self.config['database']['username']} "
            f"-p {db_type}.pass={self.config['database']['password']} "
            f"> ycsb_output.txt"
        )

        try:
            process = subprocess.Popen(ycsb_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()

            if process.returncode != 0:
                print(f"Error running YCSB benchmark: {stderr.decode()}")
            else:
                print("YCSB benchmark completed successfully. Metrics are saved in 'ycsb_output.txt'.")

        except Exception as e:
            print(f"Error: {e}")

    def teardown(self):
        print("Tearing down YCSB test...")
