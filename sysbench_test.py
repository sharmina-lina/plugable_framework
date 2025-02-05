# Sysbench_test.py
import paramiko
import yaml
from sysbench_install import ssh_connect

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

    # Construct the sysbench prepare command
    prepare_command = (
        f"sysbench /usr/share/sysbench/oltp_common.lua "
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

    # Construct the sysbench test command
    sysbench_command = (
        f"sysbench /usr/share/sysbench/oltp_read_write.lua "
        f"--db-driver=mysql "
        f"--mysql-db={db_name} "
        f"--mysql-user={db_user} "
        f"--mysql-password={db_pass} "
        f"--mysql-host={db_host} "
        f"--mysql-port={db_port} "
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






