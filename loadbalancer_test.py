# Sysbench_test.py
import paramiko
import yaml


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

    




