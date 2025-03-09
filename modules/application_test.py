## modules/Application_test.py
import paramiko
import subprocess
import shutil
import sys
import yaml
import time
import re
import pandas as pd
import plotly.express as px


# Function to establish SSH connection
def application_connect(config):
    try:
        ssh_key_path = config['application']['key_path']
        key = paramiko.Ed25519Key.from_private_key_file(ssh_key_path)
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(config['application']['host'], username=config['application']['username'], pkey=key)
        print(f"Successfully connected to {config['application']['host']}")
        return client
    except Exception as e:
        print(f"Error: Unable to connect to {config['application']['host']}. {e}")
        sys.exit(1)

def install_redis_benchmark(client,  config):
    try:
        # Check if redis-benchmark is already installed
        print("Checking if Redis-Benchmark is installed...")
        stdin, stdout, stderr = client.exec_command("which redis-benchmark")
        output = stdout.read().decode().strip()
        
        if output:
            print("Redis-benchmark is already installed.")
        else:
            # Install redis-benchmark using the package manager
            print("Redis-Benchmark is not installed. Installing now...")
            install_command = "sudo apt-get update && sudo apt-get install -y redis-tools"
            stdin, stdout, stderr = client.exec_command(install_command)
            stdout.channel.recv_exit_status()  # Wait for installation to complete
            print("Redis Benchmark installation completed.")
    except Exception as e:
        print(f"Error checking or installing Redis Benchmark: {e}")
    

def perform_redis_benchmark_test(client, config):
    redis_command = "redis-benchmark -h 127.0.0.1 -p 6379 -n 10000 -c 50 > redis_benchmark_metrics.txt"
    kubectl_command = "/usr/local/bin/kubectl port-forward svc/redis-cart 6379:6379 &"
    output_file_path = 'redis_benchmark_metrics.txt'

    port_forward_process = None

    try:
        # Start port-forwarding in the background on the remote server
        print("Port-forwarding Redis service...")
        stdin, stdout, stderr = client.exec_command(kubectl_command)
        time.sleep(5)  # Wait for port-forwarding to establish

        # Run Redis benchmark test
        print("Running Redis Benchmark test...")
        stdin, stdout, stderr = client.exec_command(redis_command)
        stdout.channel.recv_exit_status()  # Wait for the command to complete
        print("Redis Benchmark test completed. Metrics are saved in 'redis_benchmark_metrics.txt'.")

    except FileNotFoundError as e:
        print(f"Error: {e}. Ensure 'kubectl' is installed and accessible on the remote machine.")
    except Exception as e:
        print(f"Error during Redis Benchmark test: {e}")

    finally:
        # Stop port-forwarding if it was started
        if port_forward_process:
            print("Stopping port-forwarding...")
            port_forward_process.terminate()
        else:
            print("Port-forwarding process was not initiated.")
    return output_file_path



def parse_benchmark_metrics(file_path):
    # Data structure to hold parsed data
    throughput_data = []
    latency_data = []
    
    with open(file_path, 'r') as file:
        lines = file.readlines()
        
        # Find throughput values and add to list
        throughput_pattern = re.compile(r"MSET \(10 keys\): rps=(\d+\.\d+)")
        latency_pattern = re.compile(r"(\d+\.\d+)% <= (\d+\.\d+) milliseconds")
        
        for line in lines:
            # Extract throughput values
            throughput_match = throughput_pattern.search(line)
            if throughput_match:
                throughput_data.append(float(throughput_match.group(1)))
            
            # Extract latency percentiles
            latency_match = latency_pattern.search(line)
            if latency_match:
                percentile = float(latency_match.group(1))
                latency = float(latency_match.group(2))
                latency_data.append((percentile, latency))

    # Save throughput data to CSV using pandas
    throughput_df = pd.DataFrame(throughput_data, columns=['Throughput (rps)'])
    throughput_df.to_csv('./outputs/throughput_redis_data.csv', index=False)

    # Save latency data to CSV using pandas
    latency_df = pd.DataFrame(latency_data, columns=['Percentile', 'Latency (ms)'])
    latency_df.to_csv('./outputs/latency_redis_data.csv', index=False)

    return throughput_data, latency_data




    
    
