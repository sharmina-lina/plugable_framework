## modules/Sysbench_install.py
import paramiko
import sys
import yaml


# Function to establish SSH connection
def ssh_connect(config):
    try:
        ssh_key_path = config['ssh']['key_path']
        key = paramiko.Ed25519Key.from_private_key_file(ssh_key_path)
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(config['ssh']['host'], username=config['ssh']['username'], pkey=key)
        print(f"Successfully connected to {config['ssh']['host']}")
        return client
    except Exception as e:
        print(f"Error: Unable to connect to {config['ssh']['host']}. {e}")
        sys.exit(1)

# Function to check if sysbench is installed on remote VM
def install_sysbench(client, config):
    print("Checking if sysbench is installed...")
    stdin, stdout, stderr = client.exec_command("sysbench --version")
    sysbench_version = stdout.read().decode().strip()
    
    if "sysbench" in sysbench_version:
        print(f"Sysbench is installed: {sysbench_version}")
    else:
        print("Sysbench is not installed. Installing sysbench...")
        
        # Updating package list and installing sysbench
        install_command = "sudo apt-get update -y && sudo apt-get install -y sysbench"
        
        # Execute the command
        stdin, stdout, stderr = client.exec_command(install_command)
        
        # Wait for the command to complete
        exit_status = stdout.channel.recv_exit_status()
        
        # Capture the output and errors
        install_output = stdout.read().decode().strip()
        install_error = stderr.read().decode().strip()
        
        if exit_status == 0:
            print("Sysbench installed successfully.")
            print(install_output)
        else:
            print("Error installing sysbench:")
            print(install_error)

