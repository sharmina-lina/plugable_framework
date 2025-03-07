# plugins/online_testing_plugin.py
from plugins.plugin_manager import Plugin
from modules.application_load_test import application_connect  # Assuming you have an SSH utility
from modules.monitoring import collect_system_metrics  # Custom function to collect metrics
from modules.sysbench_install import ssh_connect
import pandas as pd
import time
from prometheus_client import Gauge, start_http_server


class OnlineTestingPlugin(Plugin):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.client = None
        self.metrics = {}
        # Define Prometheus metrics
        self.cpu_usage_gauge = Gauge('cpu_usage_percent', 'Current CPU usage in percent')
        self.memory_usage_gauge = Gauge('memory_usage_percent', 'Current memory usage in percent')
        self.disk_read_gauge = Gauge('disk_read_ops', 'Disk read operations per second')
        self.disk_write_gauge = Gauge('disk_write_ops', 'Disk write operations per second')
        self.network_rx_gauge = Gauge('network_bytes_received', 'Bytes received on the network interface')
        self.network_tx_gauge = Gauge('network_bytes_transmitted', 'Bytes transmitted on the network interface')

    def setup(self):
        """
        Set up the SSH connection to the remote server.
        """
        print("Setting up online testing plugin...")
        self.client = application_connect(self.config)
        if self.client:
            print("SSH connection established successfully.")
        else:
            print("Failed to establish SSH connection. Exiting.")
            return False
        
        # Start Prometheus HTTP server on port 9000
        start_http_server(9000)
        print("Prometheus metrics server started on port 9000.")

    def run(self):
        """
        Perform real-time monitoring and evaluation of the remote server.
        """
        print("Running online testing...")

        try:
            while True:  # Run in a continuous loop
                try:
       

                    # Collect system metrics (CPU, memory, etc.)
                    print("Collecting system metrics...")
                    metrics = collect_system_metrics(self.client)

                    # Save metrics to a file (optional)
                    self._save_metrics_to_file(metrics)

                    # Update Prometheus metrics
                    self.cpu_usage_gauge.set(metrics['cpu_usage'])
                    self.memory_usage_gauge.set(metrics['memory_usage'])
                    self.disk_read_gauge.set(metrics['disk_read_ops'])
                    self.disk_write_gauge.set(metrics['disk_write_ops'])
                    self.network_rx_gauge.set(metrics['bytes_received'])
                    self.network_tx_gauge.set(metrics['bytes_transmitted'])

                    print("Metrics updated in Prometheus.")

                except Exception as e:
                    print(f"Error updating metrics: {e}")
        
                time.sleep(15)

        except KeyboardInterrupt:
            print("\nKeyboard interrupt detected. Stopping the plugin...")
        finally:
            # Ensure resources are cleaned up
            self.teardown()

        return True

    def teardown(self):
        """
        Clean up resources (e.g., close SSH connection).
        """
        print("Tearing down online testing plugin...")
        if self.client:
            self.client.close()
            print("SSH connection closed.")

    def _save_metrics_to_file(self, metrics):
        """
        Save collected metrics to a CSV file for analysis.
        """
        if metrics:
            print("Saving metrics to CSV...")
            df = pd.DataFrame([metrics])
            df.to_csv('./outputs/online_metrics.csv', index=False)
        else:
            print("No metrics collected. Skipping file save.")

    def teardown(self):
        print("Tearing down Online system testing ...")
        if self.client:
            self.client.close()
    
