#file_transfer.py
from scp import SCPClient
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