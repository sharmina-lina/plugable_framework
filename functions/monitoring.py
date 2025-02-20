# functions/monitoring.py
def collect_system_metrics(client):
    """
    Collect system metrics (CPU, memory, disk I/O, network I/O) from the remote server.
    """
    # Initialize metrics with default values
    metrics = {
        'cpu_usage': 0.0,
        'memory_usage': 0.0,
        'disk_read_ops': 0.0,
        'disk_write_ops': 0.0,
        'bytes_received': 0.0,
        'bytes_transmitted': 0.0
    }

    try:
        # Collect CPU usage
        stdin, stdout, stderr = client.exec_command("top -bn1 | grep 'Cpu(s)' | awk '{print $2}'")
        cpu_output = stdout.read().decode().strip()
        cpu_error = stderr.read().decode().strip()
        print(f"CPU Output: {cpu_output}")
        print(f"CPU Error: {cpu_error}")
        if cpu_output:
            metrics['cpu_usage'] = float(cpu_output)
        else:
            print("Warning: Failed to collect CPU usage.")

        # Collect memory usage
        stdin, stdout, stderr = client.exec_command("free | grep Mem | awk '{print $3/$2 * 100.0}'")
        memory_output = stdout.read().decode().strip()
        memory_error = stderr.read().decode().strip()
        print(f"Memory Output: {memory_output}")
        print(f"Memory Error: {memory_error}")
        if memory_output:
            metrics['memory_usage'] = float(memory_output)
        else:
            print("Warning: Failed to collect memory usage.")

        # Collect disk I/O (example: read/write operations per second)
        stdin, stdout, stderr = client.exec_command("iostat -d | grep '^sd' | awk '{print $2,$3}'")
        disk_output = stdout.read().decode().strip()
        disk_error = stderr.read().decode().strip()
        print(f"Disk Output: {disk_output}")
        print(f"Disk Error: {disk_error}")
        if disk_output:
            disk_read, disk_write = disk_output.split()
            metrics['disk_read_ops'] = float(disk_read)
            metrics['disk_write_ops'] = float(disk_write)
        else:
            print("Warning: Failed to collect disk I/O metrics.")

        # Collect network I/O (example: bytes received/transmitted)
        stdin, stdout, stderr = client.exec_command("cat /proc/net/dev | grep 'ens3' | awk '{print $2,$10}'")
        network_output = stdout.read().decode().strip()
        network_error = stderr.read().decode().strip()
        print(f"Network Output: {network_output}")
        print(f"Network Error: {network_error}")
        if network_output:
            bytes_received, bytes_transmitted = network_output.split()
            metrics['bytes_received'] = float(bytes_received)
            metrics['bytes_transmitted'] = float(bytes_transmitted)
        else:
            print("Warning: Failed to collect network I/O metrics.")

    except Exception as e:
        print(f"Error collecting metrics: {e}")

    return metrics