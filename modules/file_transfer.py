#modules/file_transfer.py
from scp import SCPClient
import pandas as pd
import os

# Function to transfer file from remote to local machine

def transfer_file_from_vm(client, remote_path, local_path):
    # Ensure the output directory exists
    os.makedirs(os.path.dirname(local_path), exist_ok=True)

    with SCPClient(client.get_transport()) as scp:
        scp.get(remote_path, local_path)
        print(f"File transferred from {remote_path} to {local_path}")

def transfer_file_to_vm(client, local_path, remote_path):
    # Ensure the output directory exists
    os.makedirs(os.path.dirname(remote_path), exist_ok=True)

    with SCPClient(client.get_transport()) as scp:
        scp.put(local_path, remote_path)
        print(f"File transferred from {local_path} to {remote_path}")

def _save_metrics_to_file(metrics):
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