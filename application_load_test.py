## Application__load_test.py
import sys
import paramiko
import json
import plotly.express as px
import pandas as pd
import os

# Function to establish SSH connection
def application_connect(config):
    try:
        ssh_key_path = config['application']['key_path']
        key = paramiko.RSAKey.from_private_key_file(ssh_key_path)
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(config['application']['host'], username=config['application']['username'], pkey=key)
        print(f"Successfully connected to {config['application']['host']}")
        return client
    except Exception as e:
        print(f"Error: Unable to connect to {config['application']['host']}. {e}")
        sys.exit(1)

def install_k6(client,  config):
    try:
        # Check if redis-benchmark is already installed
        print("Checking if K6 is installed...")
        stdin, stdout, stderr = client.exec_command("which k6")
        output = stdout.read().decode().strip()
        
        if output:
            print("K6 is already installed.")
        else:
            # Install K6 using the package manager
            print("K6 is not installed. Installing now...")
            install_command = "sudo apt-get update && sudo apt-get install k6"
            stdin, stdout, stderr = client.exec_command(install_command)
            stdout.channel.recv_exit_status()  # Wait for installation to complete
            print("K6 installation completed.")
    except Exception as e:
        print(f"Error checking or installing k6: {e}")

def perform_k6_test(client, config):
    
    # Define the path to the k6 script on the remote VM
    k6_script_path = 'script.js'
    
    # Define the k6 command (redirect both stdout and stderr to the output file)
    k6_command = f"k6 run --out json={k6_script_path}_result.json {k6_script_path} "
    output_file_path = f"{k6_script_path}_result.json"

    # Generate the k6 script on the remote VM
   
    try:

        # Run K6 test
        print("Running K6 test...")
        stdin, stdout, stderr = client.exec_command(k6_command)
        stdout.channel.recv_exit_status()  # Wait for the command to complete
        print("K6 Load test completed. Metrics are saved in 'k6_metrics.json'.")

    except FileNotFoundError as e:
        print(f"Error: {e}. Ensure 'k6' is installed and accessible on the remote machine.")
    except Exception as e:
        print(f"Error during K6 load test: {e}")

    return output_file_path

def parse_k6_results(json_file_path):
    try:
        # Check if the file exists
        if not os.path.exists(json_file_path):
            print(f"Error: File not found at {json_file_path}")
            return None
        
        # Initialize a dictionary to store aggregated metrics
        metrics = {
            "http_req_duration": [],
            "http_reqs": [],
            "iterations": []
        }

        # Read the file line by line
        with open(json_file_path, 'r') as f:
            for line in f:
                try:
                    # Parse each line as a JSON object
                    data = json.loads(line)
                    
                    # Extract relevant metrics
                    if data.get("metric") == "http_req_duration" and "data" in data and "value" in data["data"]:
                        metrics["http_req_duration"].append(data["data"]["value"])
                    elif data.get("metric") == "http_reqs" and "data" in data and "value" in data["data"]:
                        metrics["http_reqs"].append(data["data"]["value"])
                    elif data.get("metric") == "iterations" and "data" in data and "value" in data["data"]:
                        metrics["iterations"].append(data["data"]["value"])
                except json.JSONDecodeError as e:
                    print(f"Error parsing JSON line: {e}")
                    continue

        # Calculate metrics for HTTP request duration
        http_req_duration_metrics = {
            "avg": sum(metrics["http_req_duration"]) / len(metrics["http_req_duration"]) if metrics["http_req_duration"] else 0,
            "min": min(metrics["http_req_duration"]) if metrics["http_req_duration"] else 0,
            "max": max(metrics["http_req_duration"]) if metrics["http_req_duration"] else 0,
        }

        # Calculate total HTTP requests and iterations
        http_reqs_total = sum(metrics["http_reqs"])
        iterations_total = sum(metrics["iterations"])

        print("HTTP Request Duration Metrics:", http_req_duration_metrics)
        print("Total HTTP Requests:", http_reqs_total)
        print("Total Iterations:", iterations_total)

        return http_req_duration_metrics, http_reqs_total, iterations_total
    except Exception as e:
        print(f"Error parsing JSON file: {e}")
        return None  


def visualize_k6_results(http_req_duration_metrics):
    if http_req_duration_metrics is None:
        print("No data to visualize.")
        return

    # Convert the metrics to a DataFrame
    df = pd.DataFrame({
        'Metric': ['avg', 'min', 'max'],
        'Value': [
            http_req_duration_metrics['avg'],
            http_req_duration_metrics['min'],
            http_req_duration_metrics['max']
        ]
    })

    # Create a bar chart
    fig = px.bar(df, x='Metric', y='Value', title='HTTP Request Duration Metrics')
    fig.show()
    
