# modules/plot_dashboard.py

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
    plt.savefig('./outputs/sysbench_dashboard.eps', format='eps', bbox_inches='tight')
    plt.savefig('./outputs/sysbench_dashboard.png')
    #plt.show()
    plt.close()
    
    
    # Create figures for each plot separately
    plt.figure(figsize=(7, 5))
    sns.lineplot(data=df, x='Time (s)', y='TPS', marker='o')
    plt.title('Transactions Per Second (TPS) Over Time')
    plt.xlabel('Time (seconds)')
    plt.ylabel('TPS')
    plt.grid(True)
    plt.savefig('./outputs/sys_tps_over_time.eps', format='eps', bbox_inches='tight')
    plt.close()

    plt.figure(figsize=(7, 5))
    sns.lineplot(data=df, x='Time (s)', y='QPS', marker='o', label='Total QPS')
    sns.lineplot(data=df, x='Time (s)', y='Read QPS', marker='o', label='Read QPS')
    sns.lineplot(data=df, x='Time (s)', y='Write QPS', marker='o', label='Write QPS')
    sns.lineplot(data=df, x='Time (s)', y='Other QPS', marker='o', label='Other QPS')
    plt.title('Queries Per Second (QPS) Over Time')
    plt.xlabel('Time (seconds)')
    plt.ylabel('QPS')
    plt.legend()
    plt.grid(True)
    plt.savefig('./outputs/sys_qps_over_time.eps', format='eps', bbox_inches='tight')
    plt.close()

    plt.figure(figsize=(7, 5))
    latency.drop('Sum (ms)').plot(kind='bar', color=['blue', 'green', 'red', 'purple'])
    plt.title('Latency Metrics (ms)')
    plt.ylabel('Latency (ms)')
    plt.grid(axis='y')
    plt.savefig('./outputs/sys_latency_metrics.eps', format='eps', bbox_inches='tight')
    plt.close()

    plt.figure(figsize=(7, 5))
    fairness.plot(kind='bar', color=['orange', 'cyan'])
    plt.title('Thread Fairness Metrics')
    plt.ylabel('Value')
    plt.grid(axis='y')
    plt.savefig('./outputs/sys_thread_fairness.eps', format='eps', bbox_inches='tight')
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
    plt.savefig('./outputs/ab_dashboard.eps',format='eps', bbox_inches='tight')
    #plt.show()
    plt.close()

    # Connection Times Graph
    plt.figure(figsize=(7, 5))
    connection_times.plot(kind='bar', color=['blue', 'green', 'red', 'purple'])
    plt.title('Connection Times (ms)')
    plt.ylabel('Time (ms)')
    plt.xlabel('Category')
    plt.grid(axis='y')
    plt.savefig('./outputs/ab_connection_times.eps', format='eps', bbox_inches='tight')
    plt.close()

    # Percentiles Graph
    plt.figure(figsize=(7, 5))
    percentiles.plot(kind='bar', x='Percentile', y='Time (ms)', color='orange')
    plt.title('Latency Percentiles')
    plt.ylabel('Time (ms)')
    plt.xlabel('Percentile')
    plt.grid(axis='y')
    plt.savefig('./outputs/ab_latency_percentiles.eps', format='eps', bbox_inches='tight')
    plt.close()

def plot_redis_dashboard():
    throughput_df = pd.read_csv('./outputs/throughput_redis_data.csv')
    latency_df = pd.read_csv('./outputs/latency_redis_data.csv')

    if throughput_df.empty or not throughput_df.select_dtypes(include=['number']).any().any():
        print("No numeric data to plot for throughput.")
        return
    if latency_df.empty or not latency_df.select_dtypes(include=['number']).any().any():
        print("No numeric data to plot for latency.")
        return
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
    plt.savefig('./outputs/redis_dashboard.png')
    plt.savefig('./outputs/redis_dashboard.eps',format='eps', bbox_inches='tight')  # Save the figure to file
    #plt.show()  # Display the plots
    plt.close()

    # Throughput Plot
    plt.figure(figsize=(7, 5))
    throughput_df.plot(kind='bar', color='blue', legend=False)
    plt.title('Redis Benchmark Throughput')
    plt.ylabel('Requests per Second (rps)')
    plt.xlabel('Test Run')
    plt.grid(axis='y')
    plt.savefig('./outputs/redis_throughput.eps', format='eps', bbox_inches='tight')
    plt.close()

    # Latency Plot
    plt.figure(figsize=(7, 5))
    latency_df.plot(kind='bar', x='Percentile', y='Latency (ms)', color='orange', legend=False)
    plt.title('Redis Benchmark Latency Percentiles')
    plt.ylabel('Latency (ms)')
    plt.xlabel('Percentile')
    plt.grid(axis='y')
    plt.savefig('./outputs/redis_latency_percentiles.eps', format='eps', bbox_inches='tight')
    plt.close()

def plot_k6_dashboard():

    
    try:
        # Load CSV files
        http_req_duration_df = pd.read_csv('./outputs/k6_http_req_duration.csv')
        http_reqs_df = pd.read_csv('./outputs/k6_http_reqs.csv')
        iterations_df = pd.read_csv('./outputs/k6_iterations.csv')

        # Extract relevant metrics
        if not http_req_duration_df.empty:
            http_req_duration_avg = http_req_duration_df.mean().values[0]  # Average duration
            http_req_duration_min = http_req_duration_df.min().values[0]   # Min duration
            http_req_duration_max = http_req_duration_df.max().values[0]   # Max duration
        else:
            http_req_duration_avg, http_req_duration_min, http_req_duration_max = 0, 0, 0

        total_http_reqs = http_reqs_df.sum().values[0] if not http_reqs_df.empty else 0
        total_iterations = iterations_df.sum().values[0] if not iterations_df.empty else 0

        # Create DataFrames for visualization
        throughput_df = pd.DataFrame({
            'Test Run': ['Run 1'],  # Adjust if multiple runs exist
            'Requests per Second': [total_http_reqs]
        })

        latency_df = pd.DataFrame({
            'Percentile': ['Avg', 'Min', 'Max'],
            'Latency (ms)': [http_req_duration_avg, http_req_duration_min, http_req_duration_max]
        })

        # Create subplots
        fig, axs = plt.subplots(1, 2, figsize=(15, 5))

        # Throughput Plot
        throughput_df.plot(kind='bar', x='Test Run', y='Requests per Second', ax=axs[0], color='blue', legend=False)
        axs[0].set_title('K6 Load Test Throughput')
        axs[0].set_ylabel('Requests per Second (rps)')
        axs[0].set_xlabel('Test Run')
        axs[0].grid(axis='y')

        # Latency Plot
        latency_df.plot(kind='bar', x='Percentile', y='Latency (ms)', ax=axs[1], color='orange', legend=False)
        axs[1].set_title('K6 Load Test Latency Percentiles')
        axs[1].set_ylabel('Latency (ms)')
        axs[1].set_xlabel('Percentile')
        axs[1].grid(axis='y')

        plt.tight_layout()
        plt.savefig('./outputs/k6_dashboard.png')  # Save the figure
        plt.savefig('./outputs/k6_dashboard.eps', format='eps', bbox_inches='tight')
        plt.close()

        # Individual Plots
        # Throughput Plot
        plt.figure(figsize=(7, 5))
        throughput_df.plot(kind='bar', x='Test Run', y='Requests per Second', color='blue', legend=False)
        plt.title('K6 Load Test Throughput')
        plt.ylabel('Requests per Second (rps)')
        plt.xlabel('Test Run')
        plt.grid(axis='y')
        plt.savefig('./outputs/k6_throughput.eps', format='eps', bbox_inches='tight')
        plt.close()

        # Latency Plot
        plt.figure(figsize=(7, 5))
        latency_df.plot(kind='bar', x='Percentile', y='Latency (ms)', color='orange', legend=False)
        plt.title('K6 Load Test Latency Percentiles')
        plt.ylabel('Latency (ms)')
        plt.xlabel('Percentile')
        plt.grid(axis='y')
        plt.savefig('./outputs/k6_latency_percentiles.eps', format='eps', bbox_inches='tight')
        plt.close()

        print("Dashboard plots saved successfully!")

    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error plotting K6 dashboard: {e}")
    

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
    plt.savefig('./outputs/online_testing_dashboard.eps',format='eps', bbox_inches='tight')
    plt.close()