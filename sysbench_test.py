import paramiko
import yaml
from sysbench_install import ssh_connect

def load_config():
    with open("config.yaml", "r") as file:
        return yaml.safe_load(file)
    



def prepare_database(client, config):
    db_name = config['database']['db_name']
    db_user = config['database']['username']
    db_pass = config['database']['password']
    db_host = config['database']['host']
    db_port = config['database']['port']

    # Construct the sysbench prepare command
    prepare_command = (
        f" sysbench /usr/share/sysbench/oltp_common.lua "
        f"--db-driver=mysql "
        f"--mysql-db={db_name} "
        f"--mysql-user={db_user} "
        f"--mysql-password={db_pass} "
        f"--mysql-host={db_host} "
        f"--mysql-port={db_port} "
        f"--tables=5 "
        f"--table-size=1000000 "
        f"prepare"
    )

    try:
        # Execute the sysbench prepare command on the remote VM
        print("Preparing the database...")
        stdin, stdout, stderr = client.exec_command(prepare_command)
        
        # Read and print any error messages
        error_message = stderr.read().decode().strip()
        if error_message:
            print(f"Error during database preparation: {error_message}")
        else:
            print("Database prepared successfully.")

    except Exception as e:
        print(f"Error: {e}")

def perform_sysbench_test(client, config):
    # Extract database and test parameters from the config
    db_name = config['database']['db_name']
    db_user = config['database']['username']
    db_pass = config['database']['password']
    db_host = config['database']['host']
    db_port = config['database']['port']
    threads = 10  # Set the number of threads you want to use
    duration = 60  # Set the duration of the test in seconds

    # Construct the sysbench command
    sysbench_command = (
        f" sysbench /usr/share/sysbench/oltp_read_write.lua "
        f"--db-driver=mysql "
        f"--mysql-db={db_name} "
        f"--mysql-user={db_user} "
        f"--mysql-password={db_pass} "
        f"--mysql-host={db_host} "
        f"--mysql-port={db_port} "
        f"--tables=5 "
        f"--table-size=1000000 "
        f"--threads={threads} "
        f"--time={duration} "
        f"--report-interval=10 "
        f"--percentile=99 "
        f"run > sysbench_metrics.txt"
    )

    try:
        # Execute the sysbench command on the remote VM
        stdin, stdout, stderr = client.exec_command(sysbench_command)
        stdout.channel.recv_exit_status()  # Wait for the command to complete

        # Print sysbench output
        print("Sysbench test completed. Metrics are saved in 'sysbench_metrics.txt'.")
        
    except Exception as e:
        print(f"Error: {e}")




