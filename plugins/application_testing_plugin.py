# plugins/application_testing_plugin.py
from application_test import application_connect, perform_redis_benchmark_test,install_redis_benchmark, parse_benchmark_metrics, create_visualizations
from file_transfer import transfer_file_from_vm
from plugins.plugin_manager import Plugin

class ApplicationTestingPlugin(Plugin):
    def __init__(self, config):
        super().__init__()
        self.config = config  # Store the passed configuration
        self.client = None  # Initialize client as None

    def setup(self):
        print("Setting up Application to test...")
        

    def run(self):
        # Estblish connection
        print("Establishing connection...")
        self.client = application_connect(self.config)

        # Install packages
        install_redis_benchmark(self.client, self.config)

        # Run redis benchmark test
        print("Run the Redis benchmark test.. ")

        output_file = perform_redis_benchmark_test(self.client, self.config)
        print(f"Output file path is: {output_file}")

        # Transfer output file
        print("Transferring  redis benchmark output...")
        transfer_file_from_vm(self.client, 'redis_benchmark_metrics.txt', './outputs/redis_benchmark_result.txt')

        throughput_data, latency_data = parse_benchmark_metrics('./outputs/redis_benchmark_result.txt')
        #create_visualizations(throughput_data, latency_data)
        
        
        
        

        

    def teardown(self):
        print("Tearing down application test...")
        if self.client:
            self.client.close()
