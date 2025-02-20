# plot_dashboard.py

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json

def plot_sysbench_dashboard():
    # Load data from CSV files
    df = pd.read_csv('./outputs/sysbench_intermediate.csv')
    latency = pd.read_csv('./outputs/sysbench_latency_stats.csv', index_col=0).squeeze()
    fairness = pd.read_csv('./outputs/sysbench_fairness_stats.csv', index_col=0).squeeze()

    # Create subplots
    fig, axs = plt.subplots(2, 2, figsize=(15, 10))

    # TPS Over Time
    sns.lineplot(ax=axs[0,0], data=df, x='Time (s)', y='TPS', marker='o')
    axs[0,0].set_title('Transactions Per Second (TPS) Over Time')
    axs[0,0].set_xlabel('Time (seconds)')
    axs[0,0].set_ylabel('TPS')
    axs[0,0].grid(True)

    # QPS Over Time
    sns.lineplot(ax=axs[0,1], data=df, x='Time (s)', y='QPS', marker='o', label='Total QPS')
    sns.lineplot(ax=axs[0,1], data=df, x='Time (s)', y='Read QPS', marker='o', label='Read QPS')
    sns.lineplot(ax=axs[0,1], data=df, x='Time (s)', y='Write QPS', marker='o', label='Write QPS')
    sns.lineplot(ax=axs[0,1], data=df, x='Time (s)', y='Other QPS', marker='o', label='Other QPS')
    axs[0,1].set_title('Queries Per Second (QPS) Over Time')
    axs[0,1].set_xlabel('Time (seconds)')
    axs[0,1].set_ylabel('QPS')
    axs[0,1].legend()
    axs[0,1].grid(True)

    # Latency Metrics
    latency.drop('Sum (ms)').plot(kind='bar', ax=axs[1,0], color=['blue', 'green', 'red', 'purple'])
    axs[1,0].set_title('Latency Metrics (ms)')
    axs[1,0].set_ylabel('Latency (ms)')
    axs[1,0].set_xlabel('')
    axs[1,0].grid(axis='y')

    # Thread Fairness Metrics
    fairness.plot(kind='bar', ax=axs[1,1], color=['orange', 'cyan'])
    axs[1,1].set_title('Thread Fairness Metrics')
    axs[1,1].set_ylabel('Value')
    axs[1,1].set_xlabel('')
    axs[1,1].grid(axis='y')

    plt.tight_layout()
    plt.savefig('./outputs/sysbench_dashboard.png')
    #plt.show()
    plt.close()

def plot_ab_dashboard():
    # Load data from CSV files
    summary_stats = pd.read_csv('./outputs/ab_summary_stats.csv')
    connection_times = pd.read_csv('./outputs/ab_connection_times.csv')
    percentiles = pd.read_csv('./outputs/ab_percentiles.csv')

    # Create subplots
    fig, axs = plt.subplots(1, 2, figsize=(15, 5))

    # Connection Times
    connection_times.plot(kind='bar', ax=axs[0], color=['blue', 'green', 'red', 'purple'])
    axs[0].set_title('Connection Times (ms)')
    axs[0].set_ylabel('Time (ms)')
    axs[0].set_xlabel('Category')
    axs[0].grid(axis='y')

    # Percentiles
    percentiles.plot(kind='bar', x='Percentile', y='Time (ms)', ax=axs[1], color='orange')
    axs[1].set_title('Latency Percentiles')
    axs[1].set_ylabel('Time (ms)')
    axs[1].set_xlabel('Percentile')
    axs[1].grid(axis='y')

    plt.tight_layout()
    plt.savefig('./outputs/ab_dashboard.png')
    #plt.show()
    plt.close()

def plot_redis_dashboard():
    throughput_df = pd.read_csv('./outputs/throughput_redis_data.csv')
    latency_df = pd.read_csv('./outputs/latency_redis_data.csv')
    # Create subplots
    fig, axs = plt.subplots(1, 2, figsize=(15, 5))

    # Throughput Plot (Bar chart)
    throughput_df.plot(kind='bar', ax=axs[0], color='blue', legend=False)
    axs[0].set_title('Redis Benchmark Throughput')
    axs[0].set_ylabel('Requests per Second (rps)')
    axs[0].set_xlabel('Test Run')
    axs[0].grid(axis='y')

    # Latency Plot (Bar chart)
    latency_df.plot(kind='bar', x='Percentile', y='Latency (ms)', ax=axs[1], color='orange', legend=False)
    axs[1].set_title('Redis Benchmark Latency Percentiles')
    axs[1].set_ylabel('Latency (ms)')
    axs[1].set_xlabel('Percentile')
    axs[1].grid(axis='y')

    plt.tight_layout()
    plt.savefig('./outputs/redis_dashboard.png')  # Save the figure to file
    #plt.show()  # Display the plots
    plt.close()

def plot_k6_dashboard():
    # Load k6 metrics from the JSON file
    k6_results_path = './outputs/k6_result.json'
    
    try:
        # Parse the k6 results
        with open(k6_results_path, 'r') as f:
            k6_data = [json.loads(line) for line in f]
        
        # Extract relevant metrics
        http_req_duration = []
        http_reqs = []
        iterations = []

        for entry in k6_data:
            if entry.get("metric") == "http_req_duration" and "data" in entry and "value" in entry["data"]:
                http_req_duration.append(entry["data"]["value"])
            elif entry.get("metric") == "http_reqs" and "data" in entry and "value" in entry["data"]:
                http_reqs.append(entry["data"]["value"])
            elif entry.get("metric") == "iterations" and "data" in entry and "value" in entry["data"]:
                iterations.append(entry["data"]["value"])

        # Calculate average HTTP request duration
        http_req_duration_avg = sum(http_req_duration) / len(http_req_duration) if http_req_duration else 0

        # Create DataFrames for visualization
        throughput_df = pd.DataFrame({
            'Test Run': ['Run 1'],  # Replace with actual test run labels if available
            'Requests per Second': [sum(http_reqs)]
        })

        latency_df = pd.DataFrame({
            'Percentile': ['Avg', 'Min', 'Max'],
            'Latency (ms)': [
                http_req_duration_avg,
                min(http_req_duration) if http_req_duration else 0,
                max(http_req_duration) if http_req_duration else 0
            ]
        })

        # Create subplots
        fig, axs = plt.subplots(1, 2, figsize=(15, 5))

        # Throughput Plot (Bar chart)
        throughput_df.plot(kind='bar', x='Test Run', y='Requests per Second', ax=axs[0], color='blue', legend=False)
        axs[0].set_title('K6 Load Test Throughput')
        axs[0].set_ylabel('Requests per Second (rps)')
        axs[0].set_xlabel('Test Run')
        axs[0].grid(axis='y')

        # Latency Plot (Bar chart)
        latency_df.plot(kind='bar', x='Percentile', y='Latency (ms)', ax=axs[1], color='orange', legend=False)
        axs[1].set_title('K6 Load Test Latency Percentiles')
        axs[1].set_ylabel('Latency (ms)')
        axs[1].set_xlabel('Percentile')
        axs[1].grid(axis='y')

        plt.tight_layout()
        plt.savefig('./outputs/k6_dashboard.png')  # Save the figure to file
       # plt.show()  # Display the plots
        plt.close()

    except FileNotFoundError:
        print(f"Error: File not found at {k6_results_path}")
    except Exception as e:
        print(f"Error plotting k6 dashboard: {e}")


def plot_online_testing_dashboard():
    """
    Plot the online testing data (CPU usage, memory usage, disk I/O, network I/O).
    """
    # Load the online metrics from the CSV file
    try:
        import pandas as pd
        metrics = pd.read_csv('./outputs/online_metrics.csv')
    except FileNotFoundError:
        print("Error: Online metrics file not found.")
        return

    # Extract scalar values from the DataFrame
    cpu_usage = metrics['cpu_usage'].iloc[0]
    memory_usage = metrics['memory_usage'].iloc[0]
    disk_read_ops = metrics['disk_read_ops'].iloc[0]
    disk_write_ops = metrics['disk_write_ops'].iloc[0]
    bytes_received = metrics['bytes_received'].iloc[0]
    bytes_transmitted = metrics['bytes_transmitted'].iloc[0]

    # Create a figure with subplots
    import matplotlib.pyplot as plt
    fig, axs = plt.subplots(2, 2, figsize=(15, 10))

    # Plot CPU usage
    axs[0, 0].bar(['CPU Usage'], cpu_usage, color='blue')
    axs[0, 0].set_title('CPU Usage (%)')
    axs[0, 0].set_ylim(0, 100)

    # Plot memory usage
    axs[0, 1].bar(['Memory Usage'], memory_usage, color='green')
    axs[0, 1].set_title('Memory Usage (%)')
    axs[0, 1].set_ylim(0, 100)

    # Plot disk I/O
    axs[1, 0].bar(['Disk Read', 'Disk Write'], [disk_read_ops, disk_write_ops], color='orange')
    axs[1, 0].set_title('Disk I/O (Operations per Second)')

    # Plot network I/O
    axs[1, 1].bar(['Bytes Received', 'Bytes Transmitted'], [bytes_received, bytes_transmitted], color='red')
    axs[1, 1].set_title('Network I/O (Bytes)')

    # Adjust layout and save the plot
    plt.tight_layout()
    plt.savefig('./outputs/online_testing_dashboard.png')
    plt.close()