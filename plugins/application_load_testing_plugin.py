# plugins/application_load_testing_plugin.py
from modules.application_load_test import application_connect, install_k6, perform_k6_test, parse_k6_results, run_k6_test
from modules.file_transfer import transfer_file_from_vm, transfer_file_to_vm
from plugins.plugin_manager import Plugin
import json
from pandas import Series
import pandas as pd


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
        transfer_file_to_vm(self.client, './script/script.js', './script.js')

       # Run K6 test
        print("Run the K6 load test.. ")

        run_k6_test(self.client, self.config)
        """
        print(f"Output file path is: {output_file}")

        # Transfer output file
        print("Transferring  k6 load test output...")
        transfer_file_from_vm(self.client, f"{output_file}", './outputs/k6_result.json')
        
        """
        

        http_req_duration, http_reqs, iterations = parse_k6_results('./outputs/k6_result.json')
        http_req_duration_df = pd.DataFrame([http_req_duration])
        http_reqs_df = pd.DataFrame([http_reqs])
        iterations_df = pd.DataFrame([iterations])
        if not http_req_duration_df.empty:
            print("Saving parsed data to CSV...")
            http_req_duration_df.to_csv("./outputs/k6_http_req_duration.csv", index=False)
            http_reqs_df.to_csv('./outputs/k6_http_reqs.csv', index=False)
            iterations_df.to_csv('./outputs/k6_iterations.csv', index=False)
            
        else:
            print("Parsed data is empty. Check the input file or parsing logic.")
        
    def teardown(self):
        print("Tearing down application load test...")
        if self.client:
            self.client.close()


