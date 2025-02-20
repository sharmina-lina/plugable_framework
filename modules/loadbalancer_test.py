# modules/loadbalancer_test.py
import paramiko
import yaml
import pandas as pd
import re


def load_config():
    with open("config.yaml", "r") as file:
        return yaml.safe_load(file)
    

def install_ab(client,  config):
    try:
        # Check if `ab` is already installed
        print("Checking if Apache Benchmark (ab) is installed...")
        stdin, stdout, stderr = client.exec_command("which ab")
        output = stdout.read().decode().strip()
        
        if output:
            print("Apache Benchmark (ab) is already installed.")
        else:
            # Install `ab` using the package manager
            print("Apache Benchmark (ab) is not installed. Installing now...")
            install_command = "sudo apt-get update && sudo apt-get install -y apache2-utils"
            stdin, stdout, stderr = client.exec_command(install_command)
            stdout.channel.recv_exit_status()  # Wait for installation to complete
            print("Apache Benchmark (ab) installation completed.")
    except Exception as e:
        print(f"Error checking or installing Apache Benchmark (ab): {e}")
    
def perform_ab_test(client, config):
    # Extract database and test parameters from the config
    lb_url = config['Load_balance']['url']
    lb_num_requests = config['Load_balance']['num_requests']
    lb_concurrency = config['Load_balance']['concurrency']
    lb_duration = config['Load_balance']['test_duration']

    # Validate that all necessary parameters have values
    if not all([lb_url, lb_num_requests, lb_concurrency, lb_duration]):
        print("Missing required configuration values:")
        if not lb_url:
            print("- Load balancer URL (lb_url) is missing.")
        if not lb_num_requests:
            print("- Number of requests (lb_num_requests) is missing.")
        if not lb_concurrency:
            print("- Concurrency level (lb_concurrency) is missing.")
        if not lb_duration:
            print("- Test duration (lb_duration) is missing.")
        return

    # Construct the `ab` command for load balancer testing
    ab_command = (
        f"ab -n {lb_num_requests} -c {lb_concurrency} {lb_url} > ab_metrics.txt"
    )

    try:
        # Execute the `ab` command on the remote VM
        print("Running Apache Benchmark (ab) test...")
        stdin, stdout, stderr = client.exec_command(ab_command)
        stdout.channel.recv_exit_status()  # Wait for the command to complete

        # Print success message
        print("Apache Benchmark (ab) test completed. Metrics are saved in 'ab_metrics.txt'.")

        

    except Exception as e:
        print(f"Error during Apache Benchmark (ab) test: {e}")


def parse_ab_output(file_path):
    summary_stats = {}
    connection_times = []
    percentiles = []

    patterns = {
        "server_software": r"Server Software:\s+(.*)",
        "server_hostname": r"Server Hostname:\s+(.*)",
        "server_port": r"Server Port:\s+(\d+)",
        "document_path": r"Document Path:\s+(.*)",
        "document_length": r"Document Length:\s+(\d+) bytes",
        "concurrency_level": r"Concurrency Level:\s+(\d+)",
        "time_taken": r"Time taken for tests:\s+([\d.]+) seconds",
        "complete_requests": r"Complete requests:\s+(\d+)",
        "failed_requests": r"Failed requests:\s+(\d+)",
        "total_transferred": r"Total transferred:\s+(\d+) bytes",
        "html_transferred": r"HTML transferred:\s+(\d+) bytes",
        "requests_per_sec": r"Requests per second:\s+([\d.]+) \[#/sec\] \(mean\)",
        "time_per_request_mean": r"Time per request:\s+([\d.]+) \[ms\] \(mean\)",
        "time_per_request_concurrent": r"Time per request:\s+([\d.]+) \[ms\] \(mean, across all concurrent requests\)",
        "transfer_rate": r"Transfer rate:\s+([\d.]+) \[Kbytes/sec\] received"
    }

    connection_time_pattern = re.compile(r"(\w+):\s+(\d+)\s+(\d+)\s+([\d.]+)\s+(\d+)\s+(\d+)")
    #connection_time_pattern = re.compile(r"(\w+):\s+(\d+)\s+(\d+\.\d+)\s+\[([^\]]+)\]\s+(\d+)\s+(\d+)")
    percentile_pattern = re.compile(r"\s*(\d+)%\s+(\d+)")

    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Extract summary statistics
    for line in lines:
        for key, pattern in patterns.items():
            match = re.search(pattern, line)
            if match:
                value = match.group(1)
                # Only convert to float if it's a valid numeric value, otherwise leave as string
                try:
                    summary_stats[key] = float(value)
                except ValueError:
                    summary_stats[key] = value  # Keep it as a string if it cannot be converted

    # Extract connection times (adjust the regex to capture categories correctly)
    connection_categories = ["Connect", "Processing", "Waiting", "Total"]
    connection_times_found = False  # Flag to track if any connection time data is found
    for line in lines:
        match_connection = re.search(connection_time_pattern , line)
        if match_connection:
            category, min_val, mean_val, sd_val, median, max_val = match_connection.groups()
            if category in connection_categories:
                connection_times.append({
                    "Category": category,
                    "Min": int(min_val),
                    "Mean": float(mean_val),
                    "StdDev": float(sd_val),
                    "Median": int(median),
                    "Max": int(max_val)
                })
                connection_times_found = True

    # Extract latency percentiles (adjust the regex to capture correctly)
    for line in lines:
        match_percentile = percentile_pattern.match(line)
        if match_percentile:
            percentiles.append({
                "Percentile": int(match_percentile.group(1)),
                "Time (ms)": int(match_percentile.group(2))
            })

    # Create DataFrames if there is any data found
    connection_times_df = pd.DataFrame(connection_times) if connection_times_found else pd.DataFrame()
    percentiles_df = pd.DataFrame(percentiles)

    return summary_stats, connection_times_df, percentiles_df


    




