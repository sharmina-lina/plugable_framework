# Sysbench_test.py
import paramiko
import yaml
from functions.sysbench_install import ssh_connect
import re
import pandas as pd

def load_config():
    with open("config.yaml", "r") as file:
        return yaml.safe_load(file)
    

def execute_remote_command(client, command, output_file=None):
    """
    Execute a command on a remote machine via SSH.

    Args:
        client (paramiko.SSHClient): SSH client connected to the remote server.
        command (str): Command to execute remotely.
        output_file (str, optional): Local file to save the command's output.

    Returns:
        None
    """
    try:
        print(f"Executing sysbench command..")
        stdin, stdout, stderr = client.exec_command(command)
        stdout.channel.recv_exit_status()  # Wait for the command to complete

        # Capture output and error messages
        output = stdout.read().decode().strip()
        error = stderr.read().decode().strip()

        if output_file:
            with open(output_file, "w") as f:
                f.write(output)

        if error:
            print(f"Error during execution: {error}")
        else:
            print("Command executed successfully.")

    except Exception as e:
        print(f"Error executing remote command: {e}")
        
def prepare_database(client, config):
    """
    Prepare the database for testing using sysbench.
    """
    db_name = config['database']['db_name']
    db_user = config['database']['username']
    db_pass = config['database']['password']
    db_host = config['database']['host']
    db_port = config['database']['port']
    db_driver = config['database']['driver_name']

    # Construct the sysbench prepare command

    prepare_command = (
        f"sysbench /usr/share/sysbench/oltp_common.lua "
        f"--db-driver={db_driver} "
        f"--{db_driver}-host={db_host} "
        f"--{db_driver}-port={db_port} "
        f"--{db_driver}-user={db_user} "
        f"--{db_driver}-password={db_pass} "
        f"--{db_driver}-db={db_name} "
        f"--tables=5 "
        f"--table-size=1000000 "
        f"prepare"
    )

    # Execute the command on the remote server
    execute_remote_command(client, prepare_command)

def perform_sysbench_test(client, config):
    """
    Run the sysbench performance test on the database.
    """
    db_name = config['database']['db_name']
    db_user = config['database']['username']
    db_pass = config['database']['password']
    db_host = config['database']['host']
    db_port = config['database']['port']
    db_threads = config['database']['threads']
    db_duration = config['database']['duration']
    db_driver = config['database']['driver_name']

    # Construct the sysbench test command

    sysbench_command = (
        f"sysbench /usr/share/sysbench/oltp_read_write.lua "
        f"--db-driver={db_driver} "
        f"--{db_driver}-host={db_host} "
        f"--{db_driver}-port={db_port} "
        f"--{db_driver}-user={db_user} "
        f"--{db_driver}-password={db_pass} "
        f"--{db_driver}-db={db_name} "
        f"--tables=5 "
        f"--table-size=1000000 "
        f"--threads={db_threads} "
        f"--time={db_duration} "
        f"--report-interval=10 "
        f"--percentile=99 "
        f"run > sysbench_metrics.txt"
    )

    # Execute the command on the remote server
    execute_remote_command(client, sysbench_command)

def parse_sysbench_output(file_path):
    intermediate_results = []
    final_stats = {}
    latency_stats = {}
    fairness_stats = {}

    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Regex pattern with minor tweaks
    intermediate_pattern = re.compile(
        r'\[\s*(\d+)s\s*\]\s+thds:\s*(\d+)\s+tps:\s*([\d.]+)\s+qps:\s*([\d.]+)\s+\(r/w/o:\s*([\d.]+)/([\d.]+)/([\d.]+)\)\s+lat\s*\(ms,99%\):\s*([\d.]+)\s+err/s:\s*([\d.]+)\s+reconn/s:\s*([\d.]+)'
    )

    sql_stats_section = False
    latency_section = False
    fairness_section = False

    for line in lines:
        line = line.strip()

        # Debugging: print line being processed
        #print(f"Processing line: {line}")

        # Parse intermediate results
        match = intermediate_pattern.match(line)
        if match:
            time_sec = int(match.group(1))
            threads = int(match.group(2))
            tps = float(match.group(3))
            qps = float(match.group(4))
            read_qps = float(match.group(5))
            write_qps = float(match.group(6))
            other_qps = float(match.group(7))
            lat_99 = float(match.group(8))
            err_s = float(match.group(9))
            reconn_s = float(match.group(10))

            intermediate_results.append({
                'Time (s)': time_sec,
                'Threads': threads,
                'TPS': tps,
                'QPS': qps,
                'Read QPS': read_qps,
                'Write QPS': write_qps,
                'Other QPS': other_qps,
                'Latency 99% (ms)': lat_99,
                'Errors/s': err_s,
                'Reconnects/s': reconn_s
            })

        # Detect sections
        if line.startswith("SQL statistics:"):
            sql_stats_section = True
            continue
        if sql_stats_section:
            if line.startswith("queries performed:"):
                continue
            elif line.startswith("transactions:"):
                parts = line.split()
                final_stats['Transactions'] = int(parts[1])
                final_stats['Transactions/sec'] = float(parts[3].strip('()')) if parts[3] != 'per' else float(parts[2].strip('()'))
            elif line.startswith("queries:"):
                parts = line.split()
                final_stats['Total Queries'] = int(parts[1])
                final_stats['Queries/sec'] = float(parts[3].strip('()')) if parts[3] != 'per' else float(parts[2].strip('()'))
            elif line.startswith("ignored errors:"):
                parts = line.split()
                try:
                    final_stats['Ignored Errors'] = int(parts[2])
                    final_stats['Ignored Errors/sec'] = float(parts[4].strip('()'))
                except (IndexError, ValueError):
                    print(f"Warning: Unable to parse ignored errors line: {line}")
            elif line.startswith("reconnects:"):
                parts = line.split()
                try:
                    final_stats['Ignored Errors'] = int(parts[2])
                    final_stats['Ignored Errors/sec'] = float(parts[4].strip('()'))
                except (IndexError, ValueError):
                    print(f"Warning: Unable to parse ignored errors line: {line}")
            elif line == '':
                sql_stats_section = False

        if line.startswith("Latency (ms):"):
            latency_section = True
            continue
        if latency_section:
            if line.startswith("min:"):
                latency_stats['Min (ms)'] = float(line.split(':')[1].strip())
            elif line.startswith("avg:"):
                latency_stats['Avg (ms)'] = float(line.split(':')[1].strip())
            elif line.startswith("max:"):
                latency_stats['Max (ms)'] = float(line.split(':')[1].strip())
            elif line.startswith("99th percentile:"):
                latency_stats['99th Percentile (ms)'] = float(line.split(':')[1].strip())
            elif line.startswith("sum:"):
                latency_stats['Sum (ms)'] = float(line.split(':')[1].strip())
            elif line == '':
                latency_section = False

        if line.startswith("Threads fairness:"):
            fairness_section = True
            continue
        if fairness_section:
            if line.startswith("events (avg/stddev):"):
                parts = line.split(':')[1].strip().split('/')
                fairness_stats['Events Avg'] = float(parts[0])
                fairness_stats['Events StdDev'] = float(parts[1])
            elif line.startswith("execution time (avg/stddev):"):
                parts = line.split(':')[1].strip().split('/')
                fairness_stats['Execution Time Avg'] = float(parts[0])
                fairness_stats['Execution Time StdDev'] = float(parts[1])
            elif line == '':
                fairness_section = False

    # Convert intermediate results to DataFrame
    df_intermediate = pd.DataFrame(intermediate_results)

    return df_intermediate, final_stats, latency_stats, fairness_stats







