# plugins/application_load_testing_plugin.py
from functions.application_load_test import application_connect, install_k6, perform_k6_test, parse_k6_results, visualize_k6_results
from functions.file_transfer import transfer_file_from_vm, transfer_file_to_vm
from plugins.plugin_manager import Plugin
import json


class ApplicationLoadTestingPlugin(Plugin):
    def __init__(self, config):
        super().__init__()
        self.config = config  # Store the passed configuration
        self.client = None  # Initialize client as None
        

    def setup(self):
        print("Setting up Application Load test...")

    def run(self):

        print("Establishing connection...")
        self.client = application_connect(self.config)

        # Install K6
        install_k6(self.client, self.config)

        print("Transferring  k6_script to server...")
        transfer_file_to_vm(self.client, 'k6_script.js', './script.js')

       # Run K6 test
        print("Run the K6 load test.. ")

        output_file = perform_k6_test(self.client, self.config)
        print(f"Output file path is: {output_file}")

        # Transfer output file
        print("Transferring  k6 load test output...")
        transfer_file_from_vm(self.client, f"{output_file}", './outputs/k6_result.json')

        http_req_duration, http_reqs, iterations = parse_k6_results('./outputs/k6_result.json')
        
    def teardown(self):
        print("Tearing down application load test...")
        if self.client:
            self.client.close()


