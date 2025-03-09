# plugins/online_testing_plugin.py
from prometheus_client import Gauge, start_http_server
from plugins.plugin_manager import Plugin
from modules.application_load_test import application_connect,perform_k6_test, parse_k6_results_online
from modules.monitoring import collect_system_metrics
from modules.file_transfer import transfer_file_from_vm, transfer_file_to_vm
import time
import pandas as pd


class OnlineTestingPlugin(Plugin):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.client = None
        self.metrics = {}

        # Define Prometheus metrics for system monitoring
        self.cpu_usage_gauge = Gauge('cpu_usage_percent', 'Current CPU usage in percent')
        self.memory_usage_gauge = Gauge('memory_usage_percent', 'Current memory usage in percent')
        self.disk_read_gauge = Gauge('disk_read_ops', 'Disk read operations per second')
        self.disk_write_gauge = Gauge('disk_write_ops', 'Disk write operations per second')
        self.network_rx_gauge = Gauge('network_bytes_received', 'Bytes received on the network interface')
        self.network_tx_gauge = Gauge('network_bytes_transmitted', 'Bytes transmitted on the network interface')

        # Define Prometheus metrics for K6 load testing
        self.http_req_duration_avg_gauge = Gauge('http_req_duration_avg', 'Average HTTP request duration from K6')
        self.http_req_min_gauge = Gauge('http_req_min', 'Minimum HTTP request duration from K6')
        self.http_req_max_gauge = Gauge('http_req_max', 'Maximum HTTP request duration from K6')
        self.http_reqs_total_counter = Gauge('http_reqs_total', 'Total HTTP requests from K6')
        self.iterations_total_counter = Gauge('iterations_total', 'Total iterations from K6')

    def setup(self):
        """
        Set up the SSH connection to the remote server and start the Prometheus HTTP server.
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
    
    def run_k6_test(self):
        """
        Run the K6 load test and parse the results.
        """
        print("Running K6 load test...")

        # Transfer the K6 script to the server
        transfer_file_to_vm(self.client, 'k6_script.js', './script.js')

        # Run the K6 test
        output_file = perform_k6_test(self.client, self.config)
        print(f"K6 test output file: {output_file}")

        # Transfer the K6 output file back to the local machine
        transfer_file_from_vm(self.client, output_file, './outputs/k6_result.json')

        # Parse the K6 results
        http_req_duration, http_req_min, http_req_max, http_reqs, iterations = parse_k6_results_online('./outputs/k6_result.json')
        print(f"K6 metrics - HTTP Req Duration: {http_req_duration}, HTTP request min: {http_req_min}, HTTP request MAX: {http_req_max}  HTTP Reqs: {http_reqs}, Iterations: {iterations}")

        return {
            'http_req_duration_avg': http_req_duration,
            'http_req_duration_min': http_req_min,
            'http_req_duration_max': http_req_max,
            'http_reqs_total': http_reqs,
            'iterations_total': iterations
        }
    
    def run(self):
        """
        Perform real-time monitoring and evaluation of the remote server.
        """
        print("Running online testing...")

        try:
            # Run the K6 test and get the metrics
            k6_metrics = self.run_k6_test()
            print("K6 metrics:", k6_metrics)

            while True:  # Run in a continuous loop
                try:
                    # Collect system metrics (CPU, memory, etc.)
                    print("Collecting system metrics...")
                    metrics = collect_system_metrics(self.client)
                    print("System metrics:", metrics)

                    # Add K6 metrics to the metrics dictionary
                    metrics.update(k6_metrics)
                    print("Combined metrics:", metrics)

                    # Ensure all required columns are present
                    required_columns = [
                    'cpu_usage', 'memory_usage', 'disk_read_ops', 'disk_write_ops',
                    'bytes_received', 'bytes_transmitted', 'http_req_duration_avg',
                    'http_req_duration_min','http_req_duration_max',
                    'http_reqs_total', 'iterations_total'
                    ]
                    for column in required_columns:
                        if column not in metrics:
                            metrics[column] = 0  # Default value for missing metrics

                    # Save metrics to a file (optional)
                    self._save_metrics_to_file(metrics)

                    # Update Prometheus metrics for system monitoring
                    self.cpu_usage_gauge.set(metrics['cpu_usage'])
                    self.memory_usage_gauge.set(metrics['memory_usage'])
                    self.disk_read_gauge.set(metrics['disk_read_ops'])
                    self.disk_write_gauge.set(metrics['disk_write_ops'])
                    self.network_rx_gauge.set(metrics['bytes_received'])
                    self.network_tx_gauge.set(metrics['bytes_transmitted'])

                    print("Prometheus system metrics updated.")

                     # Update Prometheus metrics for K6 load testing
                    self.http_req_duration_avg_gauge.set(metrics.get('http_req_duration_avg', 0))
                    self.http_req_min_gauge.set(metrics.get('http_req_duration_min', 0))
                    self.http_req_max_gauge.set(metrics.get('http_req_duration_max', 0))
                    self.http_reqs_total_counter.set(metrics.get('http_reqs_total', 0))
                    self.iterations_total_counter.set(metrics.get('iterations_total', 0))

                    print("Metrics updated in Prometheus.")

                except Exception as e:
                    print(f"Error updating metrics: {e}")

                time.sleep(15)  # Adjust the interval as needed

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
            print("Saving metrics to CSV....")
            columns = [
            'cpu_usage', 'memory_usage', 'disk_read_ops', 'disk_write_ops',
            'bytes_received', 'bytes_transmitted', 'http_req_duration_avg','http_req_duration_min','http_req_duration_max',
            'http_reqs_total', 'iterations_total'
        ]

            df = pd.DataFrame([metrics],columns=columns)
            df.to_csv('./outputs/online_metrics.csv', mode='a', header=not pd.io.common.file_exists('./outputs/online_metrics.csv'), index=False)
        else:
            print("No metrics collected. Skipping file save.")
