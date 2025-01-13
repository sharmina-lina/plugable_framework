# parse_ab.py
import re
import pandas as pd

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

