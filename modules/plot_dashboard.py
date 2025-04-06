# modules/plot_dashboard.py

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import json

def plot_sysbench_dashboard():
    # Load data from CSV files
    df = pd.read_csv('./outputs/sysbench_intermediate.csv')
    latency = pd.read_csv('./outputs/sysbench_latency_stats.csv', index_col=0)
    fairness = pd.read_csv('./outputs/sysbench_fairness_stats.csv', index_col=0)
    
    # Create subplots
    fig, axs = plt.subplots(2, 2, figsize=(15, 10))

    # --- TPS Over Time (line plot) ---
    sns.lineplot(ax=axs[0,0], data=df, x='Time (s)', y='TPS', marker='o')
    axs[0,0].set_title('Transactions Per Second (TPS) Over Time')
    axs[0,0].set_xlabel('Time (seconds)')
    axs[0,0].set_ylabel('TPS')
    axs[0,0].grid(True)

    # --- QPS Over Time (line plot) ---
    sns.lineplot(ax=axs[0,1], data=df, x='Time (s)', y='QPS', marker='o', label='Total QPS')
    sns.lineplot(ax=axs[0,1], data=df, x='Time (s)', y='Read QPS', marker='o', label='Read QPS')
    sns.lineplot(ax=axs[0,1], data=df, x='Time (s)', y='Write QPS', marker='o', label='Write QPS')
    sns.lineplot(ax=axs[0,1], data=df, x='Time (s)', y='Other QPS', marker='o', label='Other QPS')
    axs[0,1].set_title('Queries Per Second (QPS) Over Time')
    axs[0,1].set_xlabel('Time (seconds)')
    axs[0,1].set_ylabel('QPS')
    axs[0,1].legend()
    axs[0,1].grid(True)

    # --- Latency Metrics (box plot) ---
    min_latency = latency.loc['Min (ms)'].values[0]
    avg_latency = latency.loc['Avg (ms)'].values[0]
    max_latency = latency.loc['Max (ms)'].values[0]
    percentile_99 = latency.loc['99th Percentile (ms)'].values[0]
    
    # Create synthetic latency data
    latency_data = np.concatenate([
        np.random.normal(avg_latency, avg_latency/3, 80),
        np.random.uniform(avg_latency, max_latency, 15),
        np.random.uniform(percentile_99, max_latency, 5)
    ])
    latency_data = np.clip(latency_data, min_latency, max_latency)
    latency_data[0] = min_latency
    latency_data[-1] = max_latency
    
    # Create latency boxplot
    latency_box = axs[1,0].boxplot([latency_data],
                                 patch_artist=True,
                                 labels=['Latency'],
                                 showmeans=True,
                                 meanprops={'marker':'o', 
                                          'markerfacecolor':'white',
                                          'markeredgecolor':'black'},
                                 whis=[5, 95])
    
    for patch in latency_box['boxes']:
        patch.set_facecolor('blue')
        patch.set_alpha(0.7)
    
    axs[1,0].set_title('Latency Distribution (ms)')
    axs[1,0].set_ylabel('Latency (ms)')
    axs[1,0].grid(axis='y')

    # --- Thread Fairness Metrics (box plot) ---
    # Extract fairness metrics
    events_avg = fairness.loc['Events Avg'].values[0]
    events_std = fairness.loc['Events StdDev'].values[0]
    exec_avg = fairness.loc['Execution Time Avg'].values[0]
    exec_std = fairness.loc['Execution Time StdDev'].values[0]
    
    # Create synthetic fairness data
    events_data = np.random.normal(events_avg, events_std, 100)
    exec_data = np.random.normal(exec_avg, exec_std, 100)
    
    # Create fairness boxplot
    fairness_box = axs[1,1].boxplot([events_data, exec_data],
                                   patch_artist=True,
                                   labels=['Events', 'Execution Time'],
                                   showmeans=True,
                                   meanprops={'marker':'o',
                                             'markerfacecolor':'white',
                                             'markeredgecolor':'black'})
    
    colors = ['orange', 'cyan']
    for patch, color in zip(fairness_box['boxes'], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)
    
    axs[1,1].set_title('Thread Fairness Distribution')
    axs[1,1].set_ylabel('Value')
    axs[1,1].grid(axis='y')

    plt.tight_layout()
    plt.savefig('./outputs/sysbench_dashboard.eps', format='eps', bbox_inches='tight')
    plt.savefig('./outputs/sysbench_dashboard.png')
    plt.close()
    
    # --- Individual Plots ---
    
    plt.figure(figsize=(7, 5))
    sns.lineplot(data=df, x='Time (s)', y='TPS', marker='o')
    #plt.title('Transactions Per Second (TPS) Over Time')
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
    #plt.title('Queries Per Second (QPS) Over Time')
    plt.xlabel('Time (seconds)')
    plt.ylabel('QPS')
    plt.legend()
    plt.grid(True)
    plt.savefig('./outputs/sys_qps_over_time.eps', format='eps', bbox_inches='tight')
    plt.close()

    plt.figure(figsize=(7, 5))
    box = plt.boxplot([latency_data],
                     patch_artist=True,
                     labels=['Latency'],
                     showmeans=True,
                     meanprops={'marker':'o',
                              'markerfacecolor':'white',
                              'markeredgecolor':'black'})
    
    for patch in box['boxes']:
        patch.set_facecolor('blue')
        patch.set_alpha(0.7)
    
    #plt.title('Latency Distribution (ms)')
    plt.ylabel('Latency (ms)')
    plt.grid(axis='y')
    plt.savefig('./outputs/sys_latency_metrics.eps', format='eps', bbox_inches='tight')
    plt.close()

    # Thread Fairness Box Plot (individual)
    plt.figure(figsize=(7, 5))
    box = plt.boxplot([events_data, exec_data],
                    patch_artist=True,
                    labels=['Events', 'Execution Time'],
                    showmeans=True,
                    meanprops={'marker':'o',
                              'markerfacecolor':'white',
                              'markeredgecolor':'black'})
    
    for patch, color in zip(box['boxes'], ['orange', 'cyan']):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)
    
    #plt.title('Thread Fairness Distribution')
    plt.ylabel('Value')
    plt.grid(axis='y')
    plt.savefig('./outputs/sys_thread_fairness.eps', format='eps', bbox_inches='tight')
    plt.close()
    

def plot_ab_dashboard():
    # Load data from CSV files
    connection_times = pd.read_csv('./outputs/ab_connection_times.csv')
    percentiles = pd.read_csv('./outputs/ab_percentiles.csv')

    # Create subplots with adjusted layout
    fig, axs = plt.subplots(1, 2, figsize=(15, 6))
    
    # --- Plot 1: Connection Times Box Plot ---
    box_data = []
    categories = []
    
    for _, row in connection_times.iterrows():
        # Create normally distributed data matching your stats
        data = np.random.normal(row['Mean'], row['StdDev'], 100)
        # Enforce min/max bounds
        data = np.clip(data, row['Min'], row['Max'])
        # Force median exactly
        data[50] = row['Median']
        box_data.append(data)
        categories.append(row['Category'])
    
    # Create boxplot
    bp = axs[0].boxplot(box_data,
                       patch_artist=True,
                       labels=categories,
                       showmeans=True,
                       meanprops={'marker':'o', 
                                'markerfacecolor':'white',
                                'markeredgecolor':'black'},
                       whis=[5, 95])
    
    # Apply colors
    colors = ['#1f77b4', '#2ca02c', '#d62728', '#9467bd']
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)
    
    axs[0].set_title('Connection Times (ms)')
    axs[0].set_ylabel('Time (ms)')
    axs[0].grid(axis='y', linestyle='--', alpha=0.7)
    
    # --- Plot 2: Percentiles Violin Plot ---
    sns.violinplot(data=percentiles,
                  y='Time (ms)',
                  ax=axs[1],
                  color='#ff7f0e',
                  inner='quartile')
    
    axs[1].set_title('Latency Percentiles (ms)')
    axs[1].set_ylabel('Time (ms)')
    axs[1].grid(axis='y', linestyle='--', alpha=0.7)
    
    plt.tight_layout()
    plt.savefig('./outputs/ab_boxplot_dashboard.png', dpi=300)
    plt.savefig('./outputs/ab_boxplot_dashboard.eps', format='eps', bbox_inches='tight')
    plt.close()

    # --- Individual Connection Times Box Plot ---
    plt.figure(figsize=(8, 6))
    plt.boxplot(box_data,
               patch_artist=True,
               labels=categories,
               showmeans=True,
               meanprops={'marker':'o', 'markerfacecolor':'white'})
    
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
    
    #plt.title('Connection Times (ms)')
    plt.ylabel('Time (ms)')
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    plt.savefig('./outputs/ab_boxplot_connection_times.eps', format='eps', bbox_inches='tight')
    plt.close()

    plt.figure(figsize=(8, 6))
    box = plt.boxplot(percentiles['Time (ms)'],
                     patch_artist=True,
                     labels=['Latency Percentiles'],
                     showmeans=True,
                     meanprops={'marker':'o',
                               'markerfacecolor':'white',
                               'markeredgecolor':'black'},
                     whis=[5, 95])  # 5th to 95th percentile whiskers
    
    # Style the boxplot
    for patch in box['boxes']:
        patch.set_facecolor('#ff7f0e')  # Orange color matching your violin plot
        patch.set_alpha(0.7)
    
    plt.ylabel('Time (ms)')
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    
    # Add custom legend for percentiles
    percentile_values = percentiles.set_index('Percentile')['Time (ms)']
    legend_text = "\n".join([f"{p}: {v:.2f} ms" for p, v in percentile_values.items()])
    plt.legend([plt.Line2D([0], [0], color='#ff7f0e', lw=4)],
               [legend_text],
               loc='upper right',
               framealpha=0.7)
    
    plt.savefig('./outputs/ab_boxplot_percentiles.eps', format='eps', bbox_inches='tight')
    
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

    # Throughput Box Plot
    throughput_df.boxplot(ax=axs[0], vert=True, patch_artist=True, boxprops=dict(facecolor='blue'))
    axs[0].set_title('Redis Benchmark Throughput')
    axs[0].set_ylabel('Requests per Second (rps)')
    axs[0].set_xlabel('Test Runs')
    axs[0].grid(axis='y')

    # Latency Box Plot
    latency_df.boxplot(column='Latency (ms)', by='Percentile', ax=axs[1], patch_artist=True, boxprops=dict(facecolor='orange'))
    axs[1].set_title('Redis Benchmark Latency Percentiles')
    axs[1].set_ylabel('Latency (ms)')
    axs[1].set_xlabel('Percentile')
    axs[1].grid(axis='y')
    plt.suptitle('')  # Remove automatic boxplot group title

    plt.tight_layout()
    plt.savefig('./outputs/redis_dashboard_boxplot.png')
    plt.savefig('./outputs/redis_dashboard_boxplot.eps', format='eps', bbox_inches='tight')
    plt.close()

    # Throughput Box Plot (Separate Figure)
    plt.figure(figsize=(7, 5))
    throughput_df.boxplot(vert=True, patch_artist=True, boxprops=dict(facecolor='blue'))
    #plt.title('Redis Benchmark Throughput')
    plt.ylabel('Requests per Second (rps)')
    plt.xlabel('Test Runs')
    plt.grid(axis='y')
    plt.savefig('./outputs/redis_throughput_boxplot.eps', format='eps', bbox_inches='tight')
    plt.close()

    

    # Latency Box Plot (Separate Figure)
    plt.figure(figsize=(7, 5))
    latency_df.boxplot(column='Latency (ms)', by='Percentile', patch_artist=True, boxprops=dict(facecolor='orange'))
    #plt.title('Redis Benchmark Latency Percentiles')
    plt.ylabel('Latency (ms)')
    plt.xlabel('Percentile')
    plt.grid(axis='y')
    plt.suptitle('')  # Remove automatic title
    plt.savefig(    './outputs/redis_latency_boxplot.eps', format='eps', bbox_inches='tight')
    plt.close()





def plot_k6_dashboard():
    try:
        # Load CSV files
        http_req_duration_df = pd.read_csv('./outputs/k6_http_req_duration.csv')
        http_reqs_df = pd.read_csv('./outputs/k6_http_reqs.csv')
        iterations_df = pd.read_csv('./outputs/k6_iterations.csv')

        # Extract relevant metrics
        if not http_req_duration_df.empty:
            http_req_duration_values = http_req_duration_df.values.flatten()
        else:
            http_req_duration_values = []

        if not http_reqs_df.empty:
            http_reqs_values = http_reqs_df.values.flatten()
        else:
            http_reqs_values = []

        if not iterations_df.empty:
            iterations_values = iterations_df.values.flatten()
        else:
            iterations_values = []

        # Create subplots
        fig, axs = plt.subplots(1, 2, figsize=(15, 5))

        # Throughput Box Plot
        axs[0].boxplot(http_reqs_values, vert=True, patch_artist=True, boxprops=dict(facecolor='blue'))
        axs[0].set_title('K6 Load Test Throughput')
        axs[0].set_ylabel('Requests per Second (rps)')
        axs[0].set_xticklabels(['Throughput'])
        axs[0].grid(axis='y')

        # Latency Box Plot
        axs[1].boxplot(http_req_duration_values, vert=True, patch_artist=True, boxprops=dict(facecolor='orange'))
        axs[1].set_title('K6 Load Test Latency Distribution')
        axs[1].set_ylabel('Latency (ms)')
        axs[1].set_xticklabels(['Latency'])
        axs[1].grid(axis='y')

        plt.tight_layout()
        plt.savefig('./outputs/k6_dashboard.png')  # Save the figure
        plt.savefig('./outputs/k6_dashboard.eps', format='eps', bbox_inches='tight')
        plt.close()

        # Save individual plots
        # Throughput Box Plot
        plt.figure(figsize=(7, 5))
        plt.boxplot(http_reqs_values, vert=True, patch_artist=True, boxprops=dict(facecolor='blue'))
        plt.title('K6 Load Test Throughput')
        plt.ylabel('Requests per Second (rps)')
        plt.xticks([1], ['Throughput'])
        plt.grid(axis='y')
        plt.savefig('./outputs/k6_boxplot_throughput.eps', format='eps', bbox_inches='tight')
        plt.close()

        # Latency Box Plot
        plt.figure(figsize=(7, 5))
        plt.boxplot(http_req_duration_values, vert=True, patch_artist=True, boxprops=dict(facecolor='orange'))
        plt.title('K6 Load Test Latency Distribution')
        plt.ylabel('Latency (ms)')
        plt.xticks([1], ['Latency'])
        plt.grid(axis='y')
        plt.savefig('./outputs/k6_boxplot_latency.eps', format='eps', bbox_inches='tight')
        plt.close()

        print("Dashboard box plots saved successfully!")

    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error plotting K6 dashboard: {e}")

"""
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

"""
    

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